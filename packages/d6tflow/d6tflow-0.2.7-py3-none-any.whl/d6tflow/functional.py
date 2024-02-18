import d6tflow.tasks as tasks
import d6tflow
from functools import wraps
import pathlib
import d6tcollect


class Workflow:
    """
        Functional Flow class that acts as a manager of all flow steps.
        Defines all the decorators that can be used on flow functions.
    """

    def __init__(self):
        self.funcs_to_run = []
        self.steps = {}
        self.instantiated_tasks = {}
        self.object_count = 0
        self.multi_params = None
        self.multi_params_tasks = {}
        self.params_used = {}

        def common_decorator(func):
            """
                Common decorator that all decorators use.
            """
            # Checking if the function that is decorated is the function that we want to run.
            # If so then we set the function as the run function for the current task class.
            # Also we are changing the name of the task class to the function name.
            if not '__wrapped__' in func.__dict__:
                self.steps[func.__name__] = self.steps[self.current_step]
                del self.steps[self.current_step]
                self.steps[func.__name__].__name__ = func.__name__
                setattr(self.steps[func.__name__], 'run', func)

            # Thanks to wraps, wrapper has all the metadata of func.
            @wraps(func)
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
            return wrapper
        self.common_decorator = common_decorator

    @d6tcollect._collectClass
    def task(self, task_type: d6tflow.tasks.TaskData):
        """
            Flow step decorator.
            Converts the decorated function into a flow step.
            Should be defined at the top of the decorator stack.

            Parameters
            ----------
            task_type : d6ftflow.tasks.TaskData
                task_type should be a class which inherits from d6ftflow.tasks.TaskData

            Example
            -------
            @flow.step(d6tflow.tasks.TaskCache)
        """
        assert task_type.__base__ == tasks.TaskData, "Invalid parameter. Parameter should be type defined in d6tflow.tasks"
        self.task_type = task_type
        step_name = str(self.object_count)
        self.steps[step_name] = type(step_name, (task_type,), {})
        self.current_step = step_name
        self.object_count += 1
        return self.common_decorator

    @d6tcollect._collectClass
    def requires(self, *args, **kwargs):
        """
            Flow requires decorator.
            Defines dependencies between flow steps.
            Internally calls d6tflow.requires which inturn calls luigi.requires.

            Parameters
            ----------
            func : dict or function or mutiple functions

            Examples
            --------
            @flow.requires({"foo": func1, "bar": func2})
            @flow.requires(func1)
        """
        if isinstance(args[0], dict):
            tasks_to_require = {}
            for key in args[0]:
                tasks_to_require[key] = self.steps[args[0][key].__name__]

            tasks_to_require = [tasks_to_require]
        else:
            tasks_to_require = [
                self.steps[func.__name__]
                for func in args
            ]

        self.steps[self.current_step] = d6tflow.requires(
            *tasks_to_require, **kwargs)(self.steps[self.current_step])

        return self.common_decorator

    @d6tcollect._collectClass
    def params(self, **params):
        """
            Flow parameters decorator.
            Use this to add parameter(s) to a particular flow task.
            Also see flow.add_global_params() to add parameters globally
            Parameters
            ----------
            **params : keyword arguments of d6tflow parameters

            Example
            -------
            @flow.params(multiplier=d6tflow.IntParameter(default=0))
        """
        for param in params:
            setattr(self.steps[self.current_step], param, params[param])
        return self.common_decorator

    @d6tcollect._collectClass
    def persists(self, to_persist: list):
        """
            Flow persists decorator.
            Takes in a list of variables that need to be persisted for the flow step.
            Parameters
            ----------
            to_persist : list

            Example
            -------
            @flow.persists(['a1', 'a2'])
        """
        self.steps[self.current_step].persist = to_persist
        return self.common_decorator

    def preview(self, func_to_preview, params: dict):
        func_params = params
        name = func_to_preview.__name__
        all_params = self.params_used.get(name, None)
        if func_params:
            d6tflow.preview(self.steps[name](**func_params))
        elif all_params:
            for params in self.params_used[name]:
                d6tflow.preview(self.steps[name](**params))
        else:
            d6tflow.preview(self.steps[name]())

    @d6tcollect._collectClass
    def run(self, funcs_to_run, params: dict = None, multi_params: dict = None, *args, **kwargs):
        """
            Runs flow steps locally. See luigi.build for additional details
            Parameters
            ----------
            funcs_to_run : function or list of functions

            params : dict
                dictionary of paramaters. Keys are param names and values are the values of params.

            Examples
            --------

            flow.run(func, params={'multiplier':2})

            flow.run([func1, func2], params={'multiplier':42})

            flow.run(func)
        """
        funcs_to_run = funcs_to_run if isinstance(
            funcs_to_run, list) else [funcs_to_run]

        if multi_params:
            self.multi_params = multi_params
            self.multi_params_tasks = {}

            for params in multi_params:
                for func in funcs_to_run:
                    self._instantiate([func], params=multi_params[params])
                    self.multi_params_tasks[params] = self.instantiated_tasks[func.__name__]
                    d6tflow.run(
                        self.multi_params_tasks[params],
                        *args,
                        **kwargs)
        else:
            # Reset to single params mode
            self.multi_params = None
            self.multi_params_tasks = {}
            self._instantiate(funcs_to_run, params=params)

            d6tflow.run(
                list(self.instantiated_tasks.values()),
                *args,
                **kwargs)

    def _instantiate(self, funcs_to_run: list, params=None):
        params = params if params else {}
        instantiated_tasks = {
            func_to_run.__name__: self.steps[func_to_run.__name__](**params)
            for func_to_run in funcs_to_run
        }
        self.instantiated_tasks.update(instantiated_tasks)
        self._update_params_used(funcs_to_run, params)

    def _update_params_used(self, funcs, params):
        funcs = funcs if isinstance(funcs, list) else [funcs]
        for func in funcs:
            params_used = self.params_used.get(func.__name__, [])
            params_used.append(params)
            self.params_used[func.__name__] = params_used

    def add_global_params(self, **params):
        """
            Adds params to flow functions.
            More like declares the params for further use.
            Parameters
            ----------
            params : dict
                dictionary of param name and param type

            Example
            -------
            flow.add_params({'multiplier': d6tflow.IntParameter(default=0)})
        """
        for step in self.steps:
            for param in params:
                setattr(self.steps[step], param, params[param])

    def outputLoad(self, func_to_run, *args, **kwargs):
        """
            Loads all or several outputs from flow step.

            Args:
                func_to_run: flow step function
                keys (list): list of data to load
                as_dict (bool): cache data in memory
                cached (bool): cache data in memory

            Returns: list or dict of all task output
        """
        if self.multi_params:
            output = {}
            for params in self.multi_params:
                print(self.multi_params_tasks[params])
                output[params] = self.multi_params_tasks[params].outputLoad(
                    *args, **kwargs)
            return output
        else:
            name = func_to_run.__name__
            if name in self.instantiated_tasks:
                return self.instantiated_tasks[name].outputLoad(*args, **kwargs)
            raise RuntimeError(
                f"The function {name} has not been run yet! Please run the function using WorkflowObject.run()")

    def outputLoadAll(self, func_to_run, *args, **kwargs):
        """
            Loads all output from flow task and its parents.

            Args:
                func_to_run: flow step function
                keys (list): list of data to load
                as_dict (bool): cache data in memory
                cached (bool): cache data in memory

            Returns: list or dict of all task output
        """
        if self.multi_params:
            output = {}
            for params in self.multi_params:
                print(self.multi_params_tasks[params])
                output[params] = {}
                tasks = d6tflow.taskflow_upstream(
                    self.multi_params_tasks[params])
                for task in tasks:
                    output[params][task.task_family] = task.outputLoad(
                        *args, **kwargs)
            return output
        else:
            name = func_to_run.__name__
            if name in self.instantiated_tasks:
                tasks = d6tflow.taskflow_upstream(
                    self.instantiated_tasks[name])
                return {
                    task.task_family: task.outputLoad(*args, **kwargs)
                    for task in tasks
                }
            raise RuntimeError(
                f"The function {name} has not been run yet! Please run the function using WorkflowObject.run()")

    def reset(self, func_to_reset, params=None, *args, **kwargs):
        """Resets a particular function. Use with `params` to reset function with the given parameters.
        If `params` is not used, `reset(func)` will reset the function with all the parameters run thus far"""
        func_params = params
        name = func_to_reset if isinstance(
            func_to_reset, str) else func_to_reset.__name__
        if func_params:
            return self.steps[name](**func_params).reset(*args, **kwargs)
        else:
            all_params = self.params_used.get(name, None)
            if all_params:
                return [
                    self.steps[name](**params).reset(*args, **kwargs)
                    for params in self.params_used[name]
                ]

    def resetAll(self, *args, **kwargs):
        """Resets all functions that are attached to the workflow object that have run at least once."""
        for name in self.steps:
            self.reset(name, params=None, *args, **kwargs)

    def delete(self, func_to_reset, *args, **kwargs):
        """Possibly dangerous! `delete(func)` will delete *all files* in the `data/func` directory of the given func.
        Useful if you want to delete all function related outputs.
        Consider using `reset(func, params)` to reset a specific func
        """
        name = func_to_reset if isinstance(
            func_to_reset, str) else func_to_reset.__name__
        task = self.steps[name]()

        path = task._getpath([])
        for f in path.parent.glob('*'):
            f.unlink()

    def deleteAll(self, *args, **kwargs):
        """Possibly dangerous! Will delete all files in the `data/` directory of the functions attached to the workflow object.
        Useful if you want to delete all outputs even the once previously run.
        Consider using `resetAll()` if you want to only reset the functions with params you have run thus far
        """
        for task_cls in self.steps:
            task = self.steps[task_cls]()
            self.delete(task.task_family)
