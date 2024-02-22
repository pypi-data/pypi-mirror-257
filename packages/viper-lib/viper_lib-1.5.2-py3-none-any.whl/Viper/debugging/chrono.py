"""
This module allows to precisely measure the execution time of one or multiple function during the execution of a program.
You can also generate execution reports.
This is made to improve the speed of your scripts.
"""


from numbers import Complex
from typing import Any, Callable, Generic, Iterable, Literal, Optional, ParamSpec, TypeVar
from time import process_time_ns

__all__ = ["ExecutionInfo", "Chrono", "print_report"]





def funcname(func : Callable) -> str:
    """
    Tries to return the fully qualified function name (including module and eventually classes).
    """
    import inspect

    mod = inspect.getmodule(func)
    if mod:
        mod = mod.__name__ + "."
    else:
        mod = ""
    
    if hasattr(func, "__name__"):
        name = func.__name__
    else:
        name = repr(func)
    
    # You need to make a ChronoWrapper for this to work:

    # class C:

    #     @chrono       -> This will receive an actual function, not a method. The wrapped function will be transformed into a method !!!
    #     def method(self):
    #         pass

    # Instead, a ChronoWrapper object should replace the basic wrapper function and it should implement the __set_name__ method!

    # if inspect.ismethod(func) or inspect.ismethoddescriptor(func):
    #     name = func.__qualname__
    
    return mod + name





Time = TypeVar("Time", bound = complex | float | int | bool)

class ExecutionInfo(Generic[Time]):

    """
    An object that holds the information about a specific run of a function.
    """

    __slots__ = {
        "function" : "The function that was executed",
        "duration" : "The duration of the execution",
        "thread" : "The thread identifier of the thread that executed the function",
        "level" : "The call level that the function was called at"
    }

    def __init__(self) -> None:
        self.function : Callable | None = None
        self.duration : Time | int = 0
        self.thread : int = 0
        self.level : int = 0

    def __str__(self) -> str:
        return "[Function {} lasted {} units of time in thread #{} at level {}]".format(self.function.__name__ if self.function else "None", self.duration, self.thread, self.level)





P = ParamSpec("P")
R = TypeVar("R")

class Chrono(Generic[Time]):

    """
    A chronometer class. Allows to measure execution time of multiple functions in a program (even at multiple levels).
    Can be used as a function decorator, timing every run of the function.

    A Chrono instance can take a custom clock function as argument. This should be a function with no arguments and should return a number.
    Careful : the default clock is process_time_ns (that measures CPU time for this process only). For example, using sleep won't make time pass.
    """

    def __init__(self, clock : Callable[[], Time] = process_time_ns) -> None:
        from typing import Dict, List, Tuple, Callable

        if not callable(clock):
            raise TypeError("Expected callable, got " + repr(clock.__class__.__name__))
        try:
            i = clock()
        except:
            raise ValueError("Clock function did not work")
        
        self.clock = clock
        self.__level : Dict[int, int] = {}
        self.__entries : List[Tuple[Time, Callable, int, int, bool]] = []         # self.__entries[i] = (time, func, level, TID, in_or_out)
        self.__enabled : bool = True
        self.__auto_report : bool = False
        def reporter():
            print_report(self)
        self.__reporter = reporter

    
    @property
    def enabled(self) -> bool:
        """
        True if this Chrono is enabled. If not, all timed function calls won't be measured.
        (It is made to reduce overhead when measures are not required.)
        """
        return self.__enabled
    

    @enabled.setter
    def enabled(self, value : bool):
        if not isinstance(value, bool):
            raise TypeError("Expected bool, got " + repr(type(value).__name__))
        self.__enabled = value
    

    @property
    def auto_report(self) -> bool:
        """
        If True, this Chrono will get its report printed before exit of the interpreter automatically.
        """
        return self.__auto_report


    @auto_report.setter
    def auto_report(self, value : bool):
        if not isinstance(value, bool):
            raise TypeError("Expected bool, got " + repr(type(value).__name__))
        import atexit
        if not self.__auto_report and value:
            atexit.register(self.__reporter)
        elif self.__auto_report and not value:
            atexit.unregister(self.__reporter)
        self.__auto_report = value

    
    def call(self, func : Callable[P, R], *args : P.args, **kwargs : P.kwargs) -> R:
        """
        Calls function with given arguments and measures its execution time.
        Returns what the function returns.
        """
        if not self.__enabled:
            return func(*args, **kwargs)

        from threading import get_ident
        TID = get_ident()
        if TID not in self.__level:
            self.__level[TID] = 0

        level = self.__level[TID]
        self.__level[TID] += 1
        self.__entries.append((self.clock(), func, level, TID, True))

        try:
            return func(*args, **kwargs)
        except:
            raise
        finally:
            self.__level[TID] -= 1
            self.__entries.append((self.clock(), func, level, TID, False))
    

    def __call__(self, func : Callable[P, R]) -> Callable[P, R]:
        """
        Implements the decorator of a function.
        A function decorated with a chrono will be timed every time it is called.
        """
        from Viper.meta.utils import signature_def, signature_call
        from functools import wraps

        sig = "@wraps(old_target)\n"

        sig_def, env = signature_def(func, init_env = {"old_target" : func, "chrono" : self.call, "wraps" : wraps})
        
        code = sig + sig_def
        
        code += "\n\t"

        code += "return chrono(old_target, "

        sig_call = signature_call(func, decorate = False)

        code += sig_call + ")"
                
        code += "\n"

        exec(code, env)

        return env[func.__name__]
    

    def results(self, *, extensive : bool = False, sort : Literal["name", "calls", "proportion", "speed"] = "name", reversed : bool = False) -> dict[Callable, list[ExecutionInfo]]:
        """
        Returns the execution times of all function, in the clock unit.

        Results are in the form:
            {
                func1 : [ExecutionInfo1, ExecutionInfo2, ...],
                func2 : ...,
                ...
            }

        If extensive is True, when a function passes to another timed function, its own chronometer keeps running.
        Otherwise, the second function's time is subtracted from the first one.

        By default, results are given in alphabetical order of extended function names. Other sorts are available:
        - "calls" sorts functions by most often called first.
        - "proportion" sorts functions by most time used first.
        - "speed" sorts function by speed order, with the fastest functions first.
        Also, reversed can be set to True to reverse these sorts.
        """
        if not isinstance(extensive, bool):
            raise TypeError("Expected bool for extensive, got " + repr(extensive.__class__.__name__))
        if not isinstance(sort, str):
            raise TypeError("Expected str for sort, got " + repr(type(sort).__name__))
        if sort not in ["name", "calls", "proportion", "speed"]:
            raise ValueError("Expected any of ('name', 'calls', 'proportion', 'speed') for sort, got " + repr(sort))
        if not isinstance(reversed, bool):
            raise TypeError("Exptected bool for reversed, got " + repr(type(reversed).__name__))

        res : dict[Callable, list[ExecutionInfo]] = {}

        entries = self.__entries.copy()
        TIDs = {TID for time, func, level, TID, entry in entries}
        for TID in TIDs:
            calls : list[tuple[Callable, Time]] = []
            last_durations : list[Time] = [0]
            for time, func, level, TID, entry in filter(lambda x : x[3] == TID, entries):
                if entry:
                    calls.append((func, time))
                    last_durations.append(0)
                else:
                    _, last_time = calls.pop()
                    duration = time - last_time
                    children_duration = last_durations.pop()
                    last_durations[-1] += duration
                    if not extensive:
                        duration -= children_duration
                    if func not in res:
                        res[func] = []
                    result = ExecutionInfo()
                    res[func].append(result)
                    result.function = func
                    result.duration = duration
                    result.level = level
                    result.thread = TID
        
        l = [func for func in res]

        def key_name(func):
            return funcname(func)
        
        def key_calls(func):
            return -len(res[func])
    
        def key_proportion(func):
            executions = res[func]
            return -sum(ex_inf.duration for ex_inf in executions)
        
        def key_speed(func):
            executions = res[func]
            return -sum(ex_inf.duration for ex_inf in executions) / len(res[func])

        match sort:
            case "name":
                key = key_name
        
            case "calls":
                key = key_calls
            
            case "proportion":
                key = key_proportion
                
            case "speed":
                key = key_speed

        l.sort(key=key, reverse=reversed)

        return {func : res[func] for func in l}





def __default_conversion(t : int | float) -> float:
    """
    Converts to seconds, assuming a float is in seconds and an integer is in nanoseconds
    """
    if isinstance(t, float):        # Already in seconds
        return t
    elif isinstance(t, int):
        return t / 1000000000       # From nanoseconds to seconds
    else:
        raise TypeError("Unable to automatically convert type '{}' to seconds".format(t.__class__.__name__))


def print_report(c : Chrono, *, to_seconds : Callable[[Any], float] = __default_conversion, extensive : bool = False, sort : Literal["name", "calls", "proportion", "speed"] = "proportion", reversed : bool = False):
    """
    Shows a report featuring the average execution time, number of executions and proportions of all functions.
    If you are using a clock with a custom unit, you should give a function to convert your time values to seconds.
    If you are using a second (float) or nanosecond (int) clock the conversion is automatic.
    """
    from typing import Iterable

    def avg(it : Iterable[int | float]) -> int | float:
        l = list(it)
        if not l:
            raise ValueError("Average of zero values")
        return sum(l) / len(l)

    if not isinstance(c, Chrono):
        raise TypeError("Expected a Chrono object, got " + repr(c.__class__.__name__))
    if not isinstance(extensive, bool):
        raise TypeError("Expected bool, got " + repr(extensive.__class__.__name__))
    if not isinstance(sort, str):
        raise TypeError("Expected str for sort, got " + repr(type(sort).__name__))
    if sort not in ["name", "calls", "proportion", "speed"]:
        raise ValueError("Expected any of ('name', 'calls', 'proportion', 'speed') for sort, got " + repr(sort))
    if not isinstance(reversed, bool):
        raise TypeError("Exptected bool for reversed, got " + repr(type(reversed).__name__))

    from Viper.format import duration

    report = c.results(extensive = extensive, sort = sort, reversed = reversed)
    non_extensive_report = c.results()
    N_func = len(report)
    total_duration = sum(sum(to_seconds(ex_inf.duration) for ex_inf in executions) for executions in non_extensive_report.values())

    if total_duration == 0:
        print("No tests were run (zero total duration)...")
        return

    print("Execution report featuring {} functions or methods, over {}.".format(N_func, duration(total_duration)))
    print("Per function results :")
    
    for func, executions in report.items():
        subtotal_duration = sum(to_seconds(ex_inf.duration) for ex_inf in executions)
        average_duration = avg(to_seconds(ex_inf.duration) for ex_inf in executions)
        proportion = subtotal_duration / total_duration
        n = len(executions)

        print("Function {:<10s}\n\tCalls : {:<5}, Total : {:^10s}, Average : {:^10s}, Proportion : {:^5s}% of the time".format(funcname(func), str(n), duration(subtotal_duration), duration(average_duration), str(round(proportion * 100, 2))))



del __default_conversion, Any, Callable, Iterable, Literal, Optional, ParamSpec, TypeVar, Complex, P, R, process_time_ns