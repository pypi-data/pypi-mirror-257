from __future__ import annotations

from abc import ABC
from io import BytesIO
from typing import TYPE_CHECKING, Callable

from pydantic import PositiveInt

from .data import (
    AppData,
    BackupData,
    DeployData,
    DomainAnalytics,
    FileInfo,
    LogsData,
    StatusData,
)
from .errors import SquareException
from .file import File
from .http import Endpoint, HTTPClient, Response
from .listeners import CaptureListenerManager

# avoid circular imports
if TYPE_CHECKING:
    from .client import Client


class AppCache:
    __slots__ = (
        '_status',
        '_logs',
        '_backup',
        '_app_data',
    )

    def __init__(self) -> None:
        """
        The `__init__` function is called when the class is instantiated.
        It sets up the instance of the class, and defines all of its
        attributes.


        :return: The instance of the class
        :rtype: None
        """
        self._status: StatusData | None = None
        self._logs: LogsData | None = None
        self._backup: BackupData | None = None
        self._app_data: AppData | None = None

    @property
    def status(self) -> StatusData:
        """
        The status function returns the status of the application.

        :return: The status of the application.
        :rtype: StatusData
        """
        return self._status

    @property
    def logs(self) -> LogsData:
        """
        The logs function the logs of the application.

        :return: The logs of your application
        :rtype: LogsData
        """
        return self._logs

    @property
    def backup(self) -> BackupData:
        """
        The backup function is used to create a backup of the application.

        :return: The value of the _backup attribute
        :rtype: BackupData
        """
        return self._backup

    @property
    def app_data(self) -> AppData:
        """
        The app_data function is a property that returns the AppData object.

        :return: The data from the app_data
        :rtype: AppData
        """
        return self._app_data

    def clear(self):
        """
        The clear function is used to clear the status, logs, backup and data
        variables.

        :param self: Refer to the class instance
        :return: None
        :rtype: None
        """
        self._status = None
        self._logs = None
        self._backup = None
        self._app_data = None

    def update(self, *args):
        """
        The update function is used to update the data of a given instance.
        It takes in an arbitrary number of arguments, and updates the
        corresponding data if it is one of the following types:
        StatusData, LogsData, BackupData or AppData.
        If any other type is provided as an argument to this function,
        a SquareException will be raised.

        :param self: Refer to the class instance
        :param args: Pass a variable number of arguments to a function
        :return: None
        :rtype: None
        """
        for arg in args:
            if isinstance(arg, StatusData):
                self._status = arg
            elif isinstance(arg, LogsData):
                self._logs = arg
            elif isinstance(arg, BackupData):
                self._backup = arg
            elif isinstance(arg, AppData):
                self._app_data = arg
            else:
                types: list = [
                    i.__name__
                    for i in [
                        StatusData,
                        LogsData,
                        BackupData,
                        AppData,
                    ]
                ]
                raise SquareException(
                    f'you must provide stats of the following types:\n{types}'
                )


class AbstractApplication(ABC):
    """Abstract application class"""


class Application:
    """Represents an application"""

    __slots__ = [
        '_client',
        '_http',
        '_listener',
        '_data',
        'cache',
        '_id',
        '_tag',
        '_desc',
        '_ram',
        '_lang',
        '_cluster',
        '_isWebsite',
        'always_avoid_listeners',
    ]

    def __init__(
        self,
        client: 'Client',
        http: HTTPClient,
        id: str,
        tag: str,
        ram: PositiveInt,
        lang: str,
        cluster: str,
        isWebsite: bool,
        desc: str | None = None,
    ) -> None:
        """
        The `__init__` function is called when the class is instantiated.
        It sets up all the attributes that are passed in as arguments,
        and does any other initialization your class needs before It's ready
        for use.


        :param self: Refer to the class instance.
        :param client: 'Client': Store a reference to the client that created
        this app.
        :param http: HTTPClient: Make http requests to the api.
        :param id: str: The id of the app.
        :param tag: str: The tag of the app.
        :param ram: PositiveInt: The amount of ram that is allocated.
        :param lang: str: The programming language of the app.
        :param cluster: str: The cluster that the app is hosted on
        :param isWebsite: bool: Whether if the app is a website
        :param desc: str | None: Define the description of the app

        :return: None
        :rtype: None
        """
        self._id: str = id
        self._tag: str = tag
        self._desc: str | None = desc
        self._ram: PositiveInt = ram
        self._lang: str = lang
        self._cluster: str = cluster
        self._isWebsite: bool = isWebsite
        self._client: 'Client' = client
        self._http: HTTPClient = http
        self._listener: CaptureListenerManager = CaptureListenerManager()
        self.cache: AppCache = AppCache()
        self.always_avoid_listeners: bool = False

    def __repr__(self) -> str:
        """
        The __repr__ function is used to create a string representation of an
        object.
        This is useful for debugging, logging and other instances where you
        would want a string representation of the object.
        The __repr__ function should return a string that would make sense to
        someone looking at the results in the interactive interpreter.


        :param self: Refer to the class instance
        :return: The class name, tag and id of the element
        """
        return f'<{self.__class__.__name__} tag={self.tag} id={self.id}>'

    @property
    def client(self) -> 'Client':
        """
        The client function is a property that returns the client object.

        :return: The client instance
        :rtype: Client
        """
        return self._client

    @property
    def id(self) -> str:
        """
        The id function is a property that returns
         the id of the application.

        :return: The id of the application
        :rtype: str
        """
        return self._id

    @property
    def tag(self) -> str:
        """
        The tag function is a property that returns the application tag.

        :return: The tag of the application
        :rtype: str
        """
        return self._tag

    @property
    def desc(self) -> str | None:
        """
        The desc function is a property that returns the description of
        the application.

        :return: The description of the application
        :rtype: str | None
        """
        return self._desc

    @property
    def ram(self) -> int:
        """
        The ram function is a property that returns
        the amount of ram allocated to the application

        :return: The application ram
        :rtype: PositiveInt
        """
        return self._ram

    @property
    def lang(
        self,
    ) -> str:
        """
        The lang function is a property that returns the application's
        programing language.

        :return: The application's programing language
        :rtype: str
        """
        return self._lang

    @property
    def cluster(
        self,
    ) -> str:
        """
        The cluster function is a property that returns the
        cluster that the application is
        running on.


        :return: The cluster that the application is running
        :rtype: str
        """
        return self._cluster

    @property
    def is_website(self) -> bool:
        """
        The is_website function is a property that returns a boolean value
        indicating whether th application is a website.

        :return: A boolean value, true or false
        :rtype: bool
        """
        return self._isWebsite

    def capture(self, endpoint: Endpoint) -> Callable:
        """
        The capture function is a decorator that can be used to add a function
        to be called when a request is made to the specified endpoint.

        :param self: Refer to the class instance.
        :param endpoint: Endpoint: Specify which endpoint the function will be
        called on
        :return: A decorator
        :rtype: Callable
        """
        allowed_endpoints: tuple[Endpoint, Endpoint, Endpoint, Endpoint] = (
            Endpoint.logs(),
            Endpoint.app_status(),
            Endpoint.backup(),
            Endpoint.app_data(),
        )

        def wrapper(func) -> None:
            """
            The wrapper function is a decorator that takes in the endpoint as
            an argument.
            It then checks if the endpoint is allowed, and if it isn't, raises
            a SquareException.
            If there's no capture_listener for that endpoint yet, it adds one
            with the function passed to wrapper().
            Otherwise, it raises another SquareException.

            :param func: Pass the function to be wrapped
            :return: The wrapper function itself
            :rtype: None
            """
            if endpoint not in allowed_endpoints:
                raise SquareException(
                    f'the endpoint to capture must be {allowed_endpoints}'
                )

            if self._listener.get_capture_listener(endpoint) is None:
                return self._listener.add_capture_listener(endpoint, func)
            raise SquareException(
                f'Already exists an capture_listener for {endpoint}'
                f'{self._listener.get_capture_listener(endpoint)}'
            )

        return wrapper

    async def data(
        self, avoid_listener: bool = None, update_cache: bool = True
    ) -> AppData:
        """
        The data function is used to retrieve the data of an app.

        :param update_cache: if True, update the application cache
        :param avoid_listener: whether the capture listener will be called
        :param self: Refer to the class instance
        :return: A AppData object
        :rtype: AppData
        """
        app_data: AppData = await self.client.app_data(self.id)
        avoid_listener = avoid_listener or self.always_avoid_listeners
        if not avoid_listener:
            endpoint: Endpoint = Endpoint.app_data()
            await self._listener.on_capture(
                endpoint=endpoint,
                before=self.cache.app_data,
                after=app_data,
            )
        if update_cache:
            self.cache.update(app_data)
        return app_data

    async def logs(
        self, avoid_listener: bool = None, update_cache: bool = True
    ) -> LogsData:
        """
        The logs function is used to get the application's logs.

        :param self: Refer to the class instance
        :param update_cache: if True, update the application cache
        :param avoid_listener: whether the capture listener will be called
        :return: A LogsData object
        :rtype: LogsData
        """
        logs: LogsData = await self.client.get_logs(self.id)
        avoid_listener = avoid_listener or self.always_avoid_listeners
        if not avoid_listener:
            endpoint: Endpoint = Endpoint.logs()
            await self._listener.on_capture(
                endpoint=endpoint, before=self.cache.logs, after=logs
            )
        if update_cache:
            self.cache.update(logs)
        return logs

    async def status(
        self, avoid_listener: bool = None, update_cache: bool = True
    ) -> StatusData:
        """
        The status function returns the status of an application.

        :param self: Refer to the class instance
        :param update_cache: if True, update the application cache
        :param avoid_listener: whether the capture listener will be called
        :return: A StatusData object
        :rtype: StatusData
        """
        status: StatusData = await self.client.app_status(self.id)
        avoid_listener = avoid_listener or self.always_avoid_listeners
        if not avoid_listener:
            endpoint: Endpoint = Endpoint.app_status()
            await self._listener.on_capture(
                endpoint=endpoint, before=self.cache.status, after=status
            )
        if update_cache:
            self.cache.update(status)
        return status

    async def backup(
        self, avoid_listener: bool = None, update_cache: bool = True
    ) -> BackupData:
        """
        The backup function is used to create a backup of the application.

        :param self: Refer to the class instance
        :param update_cache: if True, update the application cache
        :param avoid_listener: whether the capture listener will be called
        :return: A BackupData object
        :rtype: BackupData
        """
        backup: BackupData = await self.client.backup(self.id)
        avoid_listener = avoid_listener or self.always_avoid_listeners
        if not avoid_listener:
            endpoint: Endpoint = Endpoint.backup()
            await self._listener.on_capture(
                endpoint=endpoint, before=self.cache.backup, after=backup
            )
        if update_cache:
            self.cache.update(backup)
        return backup

    async def start(self) -> Response:
        """
        The start function starts the application.

        :param self: Refer to the class instance
        :return: A Response object
        :rtype: Response
        """
        response: Response = await self.client.start_app(
            self.id, avoid_listener=True
        )
        return response

    async def stop(self) -> Response:
        """
        The stop function stops the application.

        :param self: Refer to the class instance
        :return: A Response object
        :rtype: Response
        """
        response: Response = await self.client.stop_app(
            self.id, avoid_listener=True
        )
        return response

    async def restart(self) -> Response:
        """
        The restart function restarts the application.

        :param self: Refer to the class instance
        :return: The Response object
        :rtype: Response
        """
        response: Response = await self.client.restart_app(
            self.id, avoid_listener=True
        )
        return response

    async def delete(self) -> Response:
        """
        The delete function deletes the application.

        :param self: Refer to the class instance
        :return: A Response object
        :rtype: Response
        """
        response: Response = await self.client.delete_app(
            self.id, avoid_listener=True
        )
        return response

    async def commit(self, file: File) -> Response:
        """
        The commit function is used to commit the application.


        :param self: Refer to the class instance
        :param file: File: The squarecloud.File to be committed
        :return: A Response object
        :rtype: Response
        """
        response: Response = await self.client.commit(
            self.id, file=file, avoid_listener=True
        )
        return response

    async def files_list(self, path: str) -> list[FileInfo]:
        """
        The files_list function returns a list of files and folders in the
        specified directory.

        :param self: Refer to the class instance
        :param path: str: Specify the path of the file to be listed
        :return: A list of FileInfo objects.
        :rtype: list[FileInfo]
        """
        response: list[FileInfo] = await self.client.app_files_list(
            self.id,
            path,
            avoid_listener=True,
        )
        return response

    async def read_file(self, path: str) -> BytesIO:
        """
        The read_file function reads the contents of a file from an app.

        :param self: Refer to the class instance
        :param path: str: Specify the path of the file to be read
        :return: A BytesIO object
        :rtype: BytesIO
        """
        response: BytesIO = await self.client.read_app_file(
            self.id, path, avoid_listener=True
        )
        return response

    async def create_file(self, file: File, path: str) -> Response:

        """
        The create_file function creates a file in the specified path.

        :param self: Refer to the class instance
        :param file: File: Specify the file that is to be uploaded
        :param path: str: Specify the path of the file to be created
        :return: A Response object
        :rtype: Response
        """
        response: Response = await self.client.create_app_file(
            self.id,
            file,
            path,
            avoid_listener=True,
        )
        return response

    async def delete_file(self, path: str) -> Response:
        """
        The delete_file function deletes a file from the app.

        :param self: Refer to the class instance
        :param path: str: Specify the path of the file to be deleted
        :return: A Response object
        :rtype: Response
        """
        response: Response = await self.client.delete_app_file(
            self.id, path, avoid_listener=True
        )
        return response

    async def last_deploys(self) -> list[list[DeployData]]:
        """
        The last_deploys function returns a list of the last deploys for this
        application.

        :param self: Represent the instance of the class
        :param: Pass in keyword arguments as a dictionary
        :return: A list of DeployData objects
        """
        response: list[list[DeployData]] = await self.client.last_deploys(
            self.id,
            avoid_listener=True,
        )
        return response

    async def github_integration(self, access_token: str) -> str:
        """
        The create_github_integration function returns a webhook to integrate
        with a GitHub repository.

        :param self: Access the properties of the class
        :param access_token: str: Authenticate the user with GitHub
        :return: A string containing the webhook url
        """
        webhook: str = await self.client.github_integration(
            self.id,
            access_token,
            avoid_listener=True,
        )
        return webhook

    async def domain_analytics(self) -> DomainAnalytics:
        analytics: DomainAnalytics = await self.client.domain_analytics(
            self.id, avoid_listener=True
        )
        return analytics

    async def set_custom_domain(self, custom_domain: str):
        response: Response = await self.client.set_custom_domain(
            self.id, custom_domain, avoid_listener=True
        )
        return response
