__all__ = (
    # Primitive statements and functions
    'sample1', 'ego', 'require', 'resample', 'param', 'globalParameters', 'mutate', 'verbosePrint',
    # 'localPath',
    'model',
    'simulator',
    'simulation', 'require_always', 'terminate_when',
    'terminate_simulation_when', 'terminate_after',
    # 'in_initial_scenario',
    # 'sin', 'cos', 'hypot', 'max', 'min',
    'switchOn', 'switchOff',
    'dim', 'brighten', 'color',
    'setTemp', 'increase', 'decrease', 'currentTemp',
    # 'filter',
    # Prefix operators
    # 'Visible', 'NotVisible',
    # 'Front', 'Back', 'Left', 'Right',
    # 'FrontLeft', 'FrontRight', 'BackLeft', 'BackRight',
    'assign', 'group', 'prob',
    # Infix operators
    # 'FieldAt', 'RelativeTo', 'OffsetAlong', 'RelativePosition',
    # 'RelativeHeading', 'ApparentHeading',
    # 'DistanceFrom', 'AngleTo', 'AngleFrom', 'Follow', 'CanSee',
    # Primitive types
    # 'Vector', 'VectorField', 'PolygonalVectorField',
    # 'Region', 'PointSetRegion', 'RectangularRegion', 'CircularRegion', 'SectorRegion',
    # 'PolygonalRegion', 'PolylineRegion',
    # 'Workspace', 'Mutator',
    # 'Range', 'DiscreteRange', 'Options', 'Uniform', 'Discrete', 'Normal',
    # 'TruncatedNormal',
    # 'VerifaiParameter', 'VerifaiRange', 'VerifaiDiscreteRange', 'VerifaiOptions',
    # Constructible types
    'Point', 'OrientedPoint', 'Object', 'sample', 'va', 'light', 'setup', 'thermostat','timestamp','probDist',
    'television','smartLock','fan','airPurifier','smartCamera',
    # 'setup', 'smartDevice'
    # Specifiers
    # 'With',
    # 'At', 'In', 'Beyond', 'VisibleFrom', 'VisibleSpec', 'OffsetBy', 'OffsetAlongSpec',
    # 'Facing', 'FacingToward', 'ApparentlyFacing',
    # 'LeftSpec', 'RightSpec', 'Ahead', 'Behind',
    # 'Following','dummy',
    # Constants
    # 'everywhere', 'nowhere',
    # Exceptions
    # 'GuardViolation', 'PreconditionViolation', 'InvariantViolation',
    # Internal APIs 	# TODO remove?
    # 'PropertyDefault', 'Behavior', 'Monitor', 'makeTerminationAction',
    # 'BlockConclusion', 'runTryInterrupt', 'wrapStarredValue', 'callWithStarArgs',
    # 'Modifier', 'DynamicScenario'
)

# various Python types and functions used in the language but defined elsewhere
from core.geometry import sin, cos, hypot, max, min
from core.vectors import Vector, VectorField, PolygonalVectorField
from core.regions import (Region, PointSetRegion, RectangularRegion,
                                 CircularRegion, SectorRegion, PolygonalRegion, PolylineRegion,
                                 everywhere, nowhere)
from core.workspaces import Workspace
from core.distributions import (Range, DiscreteRange, Options, Uniform, Normal,
                                       TruncatedNormal)

Discrete = Options
from core.external_params import (VerifaiParameter, VerifaiRange, VerifaiDiscreteRange,
                                         VerifaiOptions)
from core.object_types import Mutator, Point, OrientedPoint, Object, sample
from core.specifiers import PropertyDefault  # TODO remove
from core.dynamics import (Monitor, DynamicScenario, GuardViolation, PreconditionViolation, InvariantViolation,
								  makeTerminationAction)

# everything that should not be directly accessible from the language is imported here:
import builtins
import collections.abc
from contextlib import contextmanager
import importlib
import sys
import random
import os.path
import traceback
import typing
from core.distributions import (RejectionException, Distribution,
                                       TupleDistribution, StarredDistribution, toDistribution,
                                       needsSampling, canUnpackDistributions, distributionFunction)
from core.geometry import normalizeAngle, apparentHeadingAtPoint
from core.object_types import _Constructible
from core.specifiers import Specifier
from core.lazy_eval import DelayedArgument, needsLazyEvaluation
from core.errors import RuntimeParseError, InvalidScenarioError
from core.vectors import OrientedVector
from core.external_params import ExternalParameter
import core.requirements as requirements

from classes import va, light, setup, thermostat, timestamp, probDist,television,smartLock,fan,airPurifier,smartCamera
import numpy as np
### Internals

activity = 0
currentScenario = None
scenarioStack = []
scenarios = []
evaluatingRequirement = False
_globalParameters = {}
lockedParameters = set()
lockedModel = None
loadingModel = False
currentSimulation = None
inInitialScenario = True
runningScenarios = set()
currentBehavior = None
simulatorFactory = None
evaluatingGuard = False


## APIs used internally by the rest of vapl

# vapl compilation

def isActive():
    """Are we in the middle of compiling a vapl module?

    The 'activity' global can be >1 when vapl modules in turn import other
    vapl modules."""
    return activity > 0


def activate(paramOverrides={}, modelOverride=None, filename=None, namespace=None):
    """Activate the veneer when beginning to compile a vapl module."""
    global activity, _globalParameters, lockedParameters, lockedModel, currentScenario
    if paramOverrides or modelOverride:
        assert activity == 0
        _globalParameters.update(paramOverrides)
        lockedParameters = set(paramOverrides)
        lockedModel = modelOverride

    activity += 1
    assert not evaluatingRequirement
    assert not evaluatingGuard
    assert currentSimulation is None
    # placeholder scenario for top-level code
    newScenario = DynamicScenario._dummy(filename, namespace)
    scenarioStack.append(newScenario)
    currentScenario = newScenario


def deactivate():
    """Deactivate the veneer after compiling a vapl module."""
    global activity, _globalParameters, lockedParameters, lockedModel
    global currentScenario, scenarios, scenarioStack, simulatorFactory
    activity -= 1
    assert activity >= 0
    assert not evaluatingRequirement
    assert not evaluatingGuard
    assert currentSimulation is None
    scenarioStack.pop()
    assert len(scenarioStack) == activity
    scenarios = []

    if activity == 0:
        lockedParameters = set()
        lockedModel = None
        currentScenario = None
        simulatorFactory = None
        _globalParameters = {}
    else:
        currentScenario = scenarioStack[-1]


# Object creation

def registerObject(obj):
    """Add a vapl object to the global list of created objects.

    This is called by the Object constructor.
    """
    if evaluatingRequirement:
        raise RuntimeParseError('tried to create an object inside a requirement')
    elif currentBehavior is not None:
        raise RuntimeParseError('tried to create an object inside a behavior')
    elif activity > 0 or currentScenario:
        assert not evaluatingRequirement
        assert isinstance(obj, _Constructible)
        currentScenario._registerObject(obj)
        if currentSimulation:
            currentSimulation.createObject(obj)


# External parameter creation

def registerExternalParameter(value):
    """Register a parameter whose value is given by an external sampler."""
    if activity > 0:
        assert isinstance(value, ExternalParameter)
        currentScenario._externalParameters.append(value)


# Function call support

def wrapStarredValue(value, lineno):
    if isinstance(value, TupleDistribution) or not needsSampling(value):
        return value
    elif isinstance(value, Distribution):
        return [StarredDistribution(value, lineno)]
    else:
        raise RuntimeParseError(f'iterable unpacking cannot be applied to {value}')


def callWithStarArgs(_func_to_call, *args, **kwargs):
    if not canUnpackDistributions(_func_to_call):
        # wrap function to delay evaluation until starred distributions are sampled
        _func_to_call = distributionFunction(_func_to_call)
    return _func_to_call(*args, **kwargs)


# Simulations

def instantiateSimulator(factory, params):
    global _globalParameters
    assert not _globalParameters  # TODO improve hack?
    _globalParameters = dict(params)
    try:
        return factory()
    finally:
        _globalParameters = {}


def beginSimulation(sim):
    global currentSimulation, currentScenario, inInitialScenario, runningScenarios
    global _globalParameters
    if isActive():
        raise RuntimeError('tried to start simulation during vapl compilation!')
    assert currentSimulation is None
    assert currentScenario is None
    assert not scenarioStack
    currentSimulation = sim
    inInitialScenario = True
    currentScenario = sim.scene.dynamicScenario
    runningScenarios = {currentScenario}
    currentScenario._bindTo(sim.scene)
    _globalParameters = dict(sim.scene.params)

    # rebind globals that could be referenced by behaviors to their sampled values
    for modName, (namespace, sampledNS, originalNS) in sim.scene.behaviorNamespaces.items():
        namespace.clear()
        namespace.update(sampledNS)


def endSimulation(sim):
    global currentSimulation, currentScenario, currentBehavior, runningScenarios
    global _globalParameters
    currentSimulation = None
    currentScenario = None
    runningScenarios = set()
    currentBehavior = None
    _globalParameters = {}

    for modName, (namespace, sampledNS, originalNS) in sim.scene.behaviorNamespaces.items():
        namespace.clear()
        namespace.update(originalNS)


def simulationInProgress():
    return currentSimulation is not None


# Requirements

@contextmanager
def executeInRequirement(scenario, boundEgo):
    global evaluatingRequirement, currentScenario
    assert not evaluatingRequirement
    evaluatingRequirement = True
    if currentScenario is None:
        currentScenario = scenario
        clearScenario = True
    else:
        assert currentScenario is scenario
        clearScenario = False
    oldEgo = currentScenario._ego
    if boundEgo:
        currentScenario._ego = boundEgo
    try:
        yield
    finally:
        evaluatingRequirement = False
        currentScenario._ego = oldEgo
        if clearScenario:
            currentScenario = None


# Dynamic scenarios

def registerDynamicScenarioClass(cls):
    scenarios.append(cls)


@contextmanager
def executeInScenario(scenario, inheritEgo=False):
    global currentScenario
    oldScenario = currentScenario
    if inheritEgo and oldScenario is not None:
        scenario._ego = oldScenario._ego  # inherit ego from parent
    currentScenario = scenario
    try:
        yield
    finally:
        currentScenario = oldScenario


def prepareScenario(scenario):
    if currentSimulation:
        verbosePrint(f'Starting scenario {scenario}', level=3)


def finishScenarioSetup(scenario):
    global inInitialScenario
    inInitialScenario = False


def startScenario(scenario):
    runningScenarios.add(scenario)


def endScenario(scenario, reason):
    runningScenarios.remove(scenario)
    verbosePrint(f'Stopping scenario {scenario} because of: {reason}', level=3)


# Dynamic behaviors

@contextmanager
def executeInBehavior(behavior):
    global currentBehavior
    oldBehavior = currentBehavior
    currentBehavior = behavior
    try:
        yield
    finally:
        currentBehavior = oldBehavior


@contextmanager
def executeInGuard():
    global evaluatingGuard
    assert not evaluatingGuard
    evaluatingGuard = True
    try:
        yield
    finally:
        evaluatingGuard = False


### Parsing support

class Modifier(typing.NamedTuple):
    name: str
    value: typing.Any
    terminator: typing.Optional[str] = None


### Primitive statements and functions

def sample1(a):
    print(a)


def ego(obj=None):
    """Function implementing loads and stores to the 'ego' pseudo-variable.

    The translator calls this with no arguments for loads, and with the source
    value for stores.
    """
    egoObject = currentScenario._ego
    if obj is None:
        if egoObject is None:
            raise RuntimeParseError('referred to ego object not yet assigned')
    elif not isinstance(obj, Object):
        raise RuntimeParseError('tried to make non-object the ego object')
    else:
        currentScenario._ego = obj
        for scenario in runningScenarios:
            if scenario._ego is None:
                scenario._ego = obj
    return egoObject


def require(reqID, req, line, prob=1):
    """Function implementing the require statement."""
    if evaluatingRequirement:
        raise RuntimeParseError('tried to create a requirement inside a requirement')
    if currentSimulation is not None:  # requirement being evaluated at runtime
        if prob >= 1 or random.random() <= prob:
            result = req()
            assert not needsSampling(result)
            if needsLazyEvaluation(result):
                raise RuntimeParseError(f'requirement on line {line} uses value'
                                        ' undefined outside of object definition')
            if not result:
                raise RejectSimulationException(f'requirement on line {line}')
    else:  # requirement being defined at compile time
        currentScenario._addRequirement(requirements.RequirementType.require,
                                        reqID, req, line, prob)


def require_always(reqID, req, line):
    """Function implementing the 'require always' statement."""
    makeRequirement(requirements.RequirementType.requireAlways, reqID, req, line)


def terminate_when(reqID, req, line):
    """Function implementing the 'terminate when' statement."""
    makeRequirement(requirements.RequirementType.terminateWhen, reqID, req, line)


def terminate_simulation_when(reqID, req, line):
    """Function implementing the 'terminate simulation when' statement."""
    makeRequirement(requirements.RequirementType.terminateSimulationWhen,
                    reqID, req, line)


def makeRequirement(ty, reqID, req, line):
    if evaluatingRequirement:
        raise RuntimeParseError(f'tried to use "{ty.value}" inside a requirement')
    elif currentBehavior is not None:
        raise RuntimeParseError(f'"{ty.value}" inside a behavior on line {line}')
    elif currentSimulation is not None:
        currentScenario._addDynamicRequirement(ty, req, line)
    else:  # requirement being defined at compile time
        currentScenario._addRequirement(ty, reqID, req, line, 1)


def terminate_after(timeLimit, terminator=None):
    if not isinstance(timeLimit, (float, int)):
        raise RuntimeParseError('"terminate after N" with N not a number')
    assert terminator in (None, 'seconds', 'steps')
    inSeconds = (terminator != 'steps')
    currentScenario._setTimeLimit(timeLimit, inSeconds=inSeconds)


def resample(dist):
    """The built-in resample function."""
    return dist.clone() if isinstance(dist, Distribution) else dist


def verbosePrint(msg, file=sys.stdout, level=1):
    """Built-in function printing a message when the verbosity is >0.

    (Or when the verbosity exceeds the specified level.)
    """
    import syntax.translator as translator
    if translator.verbosity >= level:
        if currentSimulation:
            indent = '      ' if translator.verbosity >= 3 else '  '
        else:
            indent = '  ' * activity if translator.verbosity >= 2 else '  '
        print(indent + msg, file=file)


def localPath(relpath):
    filename = traceback.extract_stack(limit=2)[0].filename
    base = os.path.dirname(filename)
    return os.path.join(base, relpath)


def simulation():
    if isActive():
        raise RuntimeParseError('used simulation() outside a behavior')
    assert currentSimulation is not None
    return currentSimulation


def simulator(sim):
    global simulatorFactory
    simulatorFactory = sim


# def in_initial_scenario():
# 	return inInitialScenario

def model(namespace, modelName):
    global loadingModel
    if loadingModel:
        raise RuntimeParseError(f'vapl world model itself uses the "model" statement')
    if lockedModel is not None:
        modelName = lockedModel
    try:
        loadingModel = True
        module = importlib.import_module(modelName)
    except ModuleNotFoundError as e:
        if e.name == modelName:
            raise InvalidScenarioError(f'could not import world model {modelName}') from None
        else:
            raise
    finally:
        loadingModel = False
    names = module.__dict__.get('__all__', None)
    if names is not None:
        for name in names:
            namespace[name] = getattr(module, name)
    else:
        for name, value in module.__dict__.items():
            if not name.startswith('_'):
                namespace[name] = value


@distributionFunction
def filter(function, iterable):
    return list(builtins.filter(function, iterable))


def param(*quotedParams, **params):
    """Function implementing the param statement."""
    global loadingModel
    if evaluatingRequirement:
        raise RuntimeParseError('tried to create a global parameter inside a requirement')
    elif currentSimulation is not None:
        raise RuntimeParseError('tried to create a global parameter during a simulation')
    for name, value in params.items():
        if name not in lockedParameters and (not loadingModel or name not in _globalParameters):
            _globalParameters[name] = toDistribution(value)
    assert len(quotedParams) % 2 == 0, quotedParams
    it = iter(quotedParams)
    for name, value in zip(it, it):
        if name not in lockedParameters:
            _globalParameters[name] = toDistribution(value)


class ParameterTableProxy(collections.abc.Mapping):
    def __init__(self, map):
        self._internal_map = map

    def __getitem__(self, name):
        return self._internal_map[name]

    def __iter__(self):
        return iter(self._internal_map)

    def __len__(self):
        return len(self._internal_map)

    def __getattr__(self, name):
        return self.__getitem__(name)  # allow namedtuple-like access

    def _clone_table(self):
        return ParameterTableProxy(self._internal_map.copy())


def globalParameters():
    return ParameterTableProxy(_globalParameters)


def mutate(*objects):  # TODO update syntax
    """Function implementing the mutate statement."""
    if evaluatingRequirement:
        raise RuntimeParseError('used mutate statement inside a requirement')
    if len(objects) == 0:
        objects = currentScenario._objects
    for obj in objects:
        if not isinstance(obj, Object):
            raise RuntimeParseError('"mutate X" with X not an object')
        obj.mutationEnabled = True


### Prefix operators

def assign(a, b):
    classes = (light, va, thermostat, timestamp,television,smartLock,fan,airPurifier,smartCamera)
    print("a,b", a, b)
    if isinstance(a, list):
        tempDict = {a[0]: b}
        for i in range(1, len(a)):
            tempDict.__setitem__(a[i], b)
        print("list", tempDict)
        return tempDict

    if (type(a) in classes):
        tempDict = {a: b}

        # if(len({tempDict})==1):
        # tempDict.__setitem__("dummy",None)
        # print(tempDict)
        print("classes1", tempDict)
        return tempDict
    if isinstance(a, setup):
        print(a,b,"generate")
        if(type(b) is not list) and (type(b) in classes):
            tempList=[]
            tempList.append(b)
            a.generate(tempList)


        else:
         a.generate(b)
        return
    else:

        print("methods", a.__name__, type(a.__name__))

        tempDict1 = {a.__name__: b}

        # if(len({tempDict1})==1):
        # tempDict1.__setitem__("dummy",None)
        # print(tempDict1)
        return tempDict1


# light
def switchOn():
    return "switchOn"


def switchOff():
    return "switchOff"


def dim():
    return "dim"


def brighten():
    return "brighten"


def color():
    return "color"


def group(device, *args):
    flag = 0
    index = 0
    output = []
    for i in args[0]:
        output.append(device(i, args[1]))
    return output


def prob(ccList, probList):
    if(type(probList) is list):
        sum=0
        for i in probList:
            if(type(i) is not float):
                raise Exception("Incorrect type. probabilities should be of type float")
            else:
                sum=sum+i
        if(sum>1):
            raise Exception("Sum of all probabilities cannot be greater than 1")
    if (type(ccList) is not list):
        print("prob1",ccList)
        tempList=[]
        tempList.append(ccList)
        ccList=tempList
        print("prob1",ccList)
    if(type(ccList) is list):
        print("prob1",ccList,"prob2",probList)
        for i in range(0, len(ccList)):

           if(type(ccList[i]) is dict):
            #temp=ccList[i].popitem()
            temp=list(ccList[i].keys())[0]
            print("temp1",temp)
            temp.probability=probList[i]
            print("temp111",temp.probability)
           else:
               print("i am here",probList[i])
               ccList[i].probability=probList[i]











# thermostat

def setTemp():
    return "setTemp"


def increase():
    return "increase"


def decrease():
    return "decrease"


def currentTemp():
    return "currentTemp"


def alexa():
    return 'alexa'
