from playwright.sync_api import Page
from utils.config import IMPLICIT_WAIT, SETTLE_TIMEOUT_S, PAGE_LOAD_TIMEOUT_S
from utils.playwright_utils import PlaywrightUtils

# Read the whole table and the filter controls in one round trip. Polling waits call
# these repeatedly while the table re-renders, and a single atomic snapshot neither
# waits for rows to exist nor fails on rows that were replaced mid-read.
JS_READ_ROWS = "() => Array.from(document.querySelectorAll('table tbody tr'), row => row.innerText)"
JS_READ_FILTERS = (
    "() => ['searchInput', 'filterRole', 'filterStatus']"
    ".map(id => (document.getElementById(id) || {}).value || '')"
)

class ListAllUsersPage():
    """Page object for the List All Users page.

    The page updates asynchronously, and its loading spinner is typically visible for
    only 10-35 ms (and not at all when paging), which is shorter than a polling interval.
    The waits below therefore check the resulting table state instead of the spinner.
    """

    def __init__(self, page: Page, logger):
        self.page_path = "/users"
        self.page = page
        self.logger = logger
        self.playwright_utils = PlaywrightUtils(self.page, self.logger)
        self.wait_for_page_load()

    # Locators
    BUTTON_BACK_TO_DASHBOARD = "//button[contains(.,'Back')]"
    INPUT_SEARCH = "#searchInput"
    SELECT_ROLE = "#filterRole"
    SELECT_STATUS = "#filterStatus"
    BUTTON_RESET_FILTERS = "//button[text()='Reset Filters']"
    TABLE_USERS = "table"
    TABLE_USERS_HEADERS = "//table/thead/tr/th"
    TABLE_USERS_ROWS = "//table/tbody/tr"
    TABLE_NO_USERS_FOUND_MESSAGE = "#noUsersCell"
    TABLE_NEXT_PAGE_BUTTON = "#nextPage"
    TABLE_PREVIOUS_PAGE_BUTTON = "#prevPage"
    LOADING_SPINNER = ".spinner"

    # Filter keys understood by filter_users()
    FILTER_KEYS = ("name", "email", "role", "status")

    # Page Object Methods
    def wait_for_page_load(self, timeout=PAGE_LOAD_TIMEOUT_S) -> None:
        """
        Wait for the List All Users page to load by checking the presence of the uri.

        Args:
            timeout: Maximum time to wait in seconds
        """
        self.logger.info("Waiting for List All Users page to load")
        self.page.wait_for_url(f"**{self.page_path}", timeout=timeout * 1000)
        # The table briefly shows a "No users found." placeholder before the first
        # request starts, so wait for the loaded content rather than any content.
        self.wait_for_table_to_settle()

    def wait_for_table_to_settle(self) -> bool:
        """
        Wait until no request is in flight and the table content has stopped changing.

        Returns:
            bool: True if the table settled within the timeout.
        """
        rendered = self.playwright_utils.wait_until(
            lambda: not self.playwright_utils.is_element_present_now(self.LOADING_SPINNER)
            and len(self._read_rows()) > 0,
            SETTLE_TIMEOUT_S,
            "the users table to be rendered",
        )
        return self.playwright_utils.wait_for_stable(self._read_rows, description="the users table") and rendered

    def go_back_to_dashboard(self) -> None:
        """
        Click the Back to Dashboard button.
        """
        self.logger.info("Clicking Back to Dashboard button")
        self.page.click(self.BUTTON_BACK_TO_DASHBOARD)

    def is_at(self):
        """
        Verify that we are on the List All Users page by checking for the presence of a mandatory element.
        Returns:
            bool: True if on the List All Users page, False otherwise.
        """
        return self.playwright_utils.is_element_present(self.INPUT_SEARCH)

    def filter_users(self, **kwargs) -> 'ListAllUsersPage':
        """
        Filter users by name, email, role, or status.

        Args:
            name: User's name
            email: User's email
            role: User's role
            status: User's status

        Args:
            kwargs: Key-value pairs representing user attributes
                to search for. Examples:
                filter_users(name="John")
                filter_users(email="john@example.com")
                filter_users(name="John", role="Admin", status="Active")
        """
        # Each step waits for the table to reflect every filter applied so far, which
        # keeps the requests serialized: without it, a slower response for an earlier
        # step could arrive last and overwrite the combined result.
        applied = {}

        if kwargs.get('name'):
            self.logger.info(f"Filtering users by name: {kwargs['name']}")
            # Typed key by key, like Selenium's send_keys, so that both frameworks fire
            # the same input events and the application does the same work in response.
            search_input = self.page.locator(self.INPUT_SEARCH)
            search_input.clear()
            search_input.press_sequentially(kwargs['name'])
            applied['name'] = kwargs['name']
            self.wait_for_filter_applied(**applied)
        elif kwargs.get('email'):
            self.logger.info(f"Filtering users by email: {kwargs['email']}")
            # Typed key by key, like Selenium's send_keys, so that both frameworks fire
            # the same input events and the application does the same work in response.
            search_input = self.page.locator(self.INPUT_SEARCH)
            search_input.clear()
            search_input.press_sequentially(kwargs['email'])
            applied['email'] = kwargs['email']
            self.wait_for_filter_applied(**applied)
        if kwargs.get('role'):
            self.logger.info(f"Filtering users by role: {kwargs['role']}")
            self.page.select_option(self.SELECT_ROLE, label=kwargs['role'])
            applied['role'] = kwargs['role']
            self.wait_for_filter_applied(**applied)
        if kwargs.get('status'):
            self.logger.info(f"Filtering users by status: {kwargs['status']}")
            self.page.select_option(self.SELECT_STATUS, label=kwargs['status'])
            applied['status'] = kwargs['status']
            self.wait_for_filter_applied(**applied)

        return self

    def wait_for_filter_applied(self, **kwargs) -> bool:
        """
        Wait until the table actually reflects the requested filters.

        Right after an input changes, the table still shows the previous result set,
        and the spinner in between is usually too short-lived to be observed.

        Returns:
            bool: True if the table matched the filters within the timeout.
        """
        criteria = [str(kwargs[key]).lower() for key in self.FILTER_KEYS if kwargs.get(key)]
        if not criteria:
            return self.wait_for_table_to_settle()

        def table_reflects_filters():
            if self.playwright_utils.is_element_present_now(self.LOADING_SPINNER):
                return False
            # A filter that legitimately matches nothing is also a final state.
            if self.playwright_utils.is_element_present_now(self.TABLE_NO_USERS_FOUND_MESSAGE):
                return True
            rows = self._read_rows()
            return bool(rows) and all(
                all(value in row.lower() for value in criteria) for row in rows
            )

        applied = self.playwright_utils.wait_until(
            table_reflects_filters, SETTLE_TIMEOUT_S, "the filters to be applied to the table"
        )
        # The matching state could still be an intermediate render, so only report it
        # once the table has stopped changing.
        return self.playwright_utils.wait_for_stable(self._read_rows, description="the users table") and applied

    def is_user_in_list(self, **kwargs) -> bool:
        """
        Check if a user with the given attributes is present in the users list.

        Args:
            kwargs: Key-value pairs representing user attributes
                to search for. Examples:
                is_user_in_list(name="John", email="john@example.com")
                is_user_in_list(role="Admin")

        Returns:
            bool: True if some displayed row matches every given attribute.
        """
        self.logger.info(f"Checking if user with attributes {kwargs} is in the list of users")
        rows = self.get_displayed_users_rows()

        # An empty table has to be reported as a miss: checking every row for a match
        # would otherwise report success simply because there was nothing to reject.
        if not rows:
            self.logger.error("The users table is empty, so the user cannot be in it")
            return False

        for row in rows:
            if all(str(value).lower() in row.lower() for value in kwargs.values()):
                self.logger.info(f"Matching user found in row: {row}")
                return True

        self.logger.error(f"No displayed row matched all of {kwargs}")
        return False

    def is_no_users_found_message_displayed(self) -> bool:
        """
        Check if the 'No users found' message is displayed.

        Returns:
            bool: True if the message is displayed, False otherwise.
        """
        self.logger.info("Checking if 'No users found' message is displayed")
        return self.playwright_utils.is_element_present(self.TABLE_NO_USERS_FOUND_MESSAGE)

    def go_to_next_page(self) -> 'ListAllUsersPage':
        """
        Go to the next page of the users list.
        """
        self.logger.info("Clicking next page button")
        rows_before = self._read_rows()
        self.page.click(self.TABLE_NEXT_PAGE_BUTTON)
        self.wait_for_rows_to_change(rows_before, "the next page to be displayed")

        return self

    def go_to_previous_page(self) -> 'ListAllUsersPage':
        """
        Go to the previous page of the users list.
        """
        self.logger.info("Clicking previous page button")
        rows_before = self._read_rows()
        self.page.click(self.TABLE_PREVIOUS_PAGE_BUTTON)
        self.wait_for_rows_to_change(rows_before, "the previous page to be displayed")

        return self

    def get_displayed_users_rows(self) -> list:
        """
        Get all user rows from the users table.

        Returns:
            list: List of strings representing user row texts.
        """
        self.logger.info("Getting all user rows from the users table")
        result = [row.inner_text() for row in self.page.locator(self.TABLE_USERS_ROWS).all()]
        self.logger.debug(f"User rows: {result}")

        return result

    def reset_filters(self) -> 'ListAllUsersPage':
        """
        Reset all applied filters.
        """
        self.logger.info("Clicking reset filters button")
        rows_before = self._read_rows()
        self.page.click(self.BUTTON_RESET_FILTERS)

        # The controls are cleared first and the table is re-queried afterwards, so
        # wait for both; otherwise the caller can read the still-filtered table and
        # conclude that nothing was reset.
        self.playwright_utils.wait_until(
            lambda: not any(self._read_filters()) and self._read_rows() != rows_before,
            SETTLE_TIMEOUT_S,
            "the filters to be cleared and the table to be refreshed",
        )
        self.wait_for_table_to_settle()

        return self

    def wait_for_rows_to_change(self, rows_before: list, description: str) -> bool:
        """
        Wait for the table to show different rows than before, then to settle.

        Paging swaps the rows without showing a spinner at all, so the change in
        content is the only reliable signal that the new page has been rendered.

        Returns:
            bool: True if the rows changed and settled within the timeout.
        """
        def rows_changed():
            rows = self._read_rows()
            return bool(rows) and rows != rows_before

        changed = self.playwright_utils.wait_until(rows_changed, SETTLE_TIMEOUT_S, description)
        return self.wait_for_table_to_settle() and changed

    def _read_rows(self) -> list:
        """Return the text of every table row, read atomically and without logging."""
        return self.page.evaluate(JS_READ_ROWS)

    def _read_filters(self) -> list:
        """Return the current values of the search, role, and status controls."""
        return self.page.evaluate(JS_READ_FILTERS)
