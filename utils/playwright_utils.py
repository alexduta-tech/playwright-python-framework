import time

from playwright.sync_api import Page

from utils.config import (
    IMPLICIT_WAIT,
    SETTLE_POLL_S,
    LOADING_APPEAR_TIMEOUT_S,
    LOADING_DISAPPEAR_TIMEOUT_S,
    SETTLE_TIMEOUT_S,
    STABLE_DWELL_S,
)

class PlaywrightUtils:
    """Utility class for Playwright-related helper methods.
    """
    
    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger
    
    def is_element_present(self, selector: str, timeout: int = 1000) -> bool:
        """
        Check if an element is present on the page with a timeout.
        Args:
            selector (str): CSS selector, XPath, or Playwright text/role selector.
            timeout (int): Maximum time to wait in milliseconds (default: 1000ms).
        Returns:
            bool: True if element is present, False otherwise.
        """
        self.logger.debug(f"Checking if element is present: {selector}")
        try:
            self.page.locator(selector).wait_for(state="attached", timeout=timeout)
            self.scroll_to_element(selector)
            self.logger.debug(f"Element is present")
            return True
        except Exception:
            self.logger.debug("Element is not present")
            return False

    def is_element_present_now(self, selector: str) -> bool:
        """Check for an element without waiting at all.

        Polling loops call this many times, so it uses an immediate count instead of
        a wait: anything else would turn a fast poll into a multi-second one.
        """
        try:
            return self.page.locator(selector).count() > 0
        except Exception:
            return False

    def wait_until(self, predicate, timeout: float, description: str = "condition", quiet: bool = False) -> bool:
        """Poll a predicate until it holds or the timeout expires.

        Returns False on timeout rather than raising, so that the calling test still
        fails on its own assertion and the reported failure describes the actual
        problem instead of a generic timeout.
        """
        deadline = time.monotonic() + timeout

        while True:
            try:
                if predicate():
                    return True
            except Exception:
                # The page may be mid-update, so a failed lookup is expected here
                pass

            if time.monotonic() >= deadline:
                # Some timeouts are an expected outcome rather than a problem
                log = self.logger.debug if quiet else self.logger.warning
                log(f"Timed out after {timeout}s waiting for {description}")
                return False

            time.sleep(SETTLE_POLL_S)

    def wait_for_loading_cycle(
        self,
        selector: str,
        appear_timeout: float = LOADING_APPEAR_TIMEOUT_S,
        disappear_timeout: float = LOADING_DISAPPEAR_TIMEOUT_S,
    ) -> None:
        """Wait for the loading cycle triggered by the previous action to complete.

        The spinner is only rendered once the request is in flight, so waiting for
        the hidden state immediately after an action succeeds straight away while
        the previous results are still on screen: a detached element already counts
        as hidden. Wait briefly for the spinner to appear first; if it never does,
        the update already completed.
        """
        self.logger.debug(f"Waiting for the loading cycle: {selector}")

        if not self.wait_until(
            lambda: self.is_element_present_now(selector), appear_timeout, "the spinner to appear",
            quiet=True,
        ):
            self.logger.debug("Spinner never appeared, assuming the update already completed")
            return

        self.wait_until(
            lambda: not self.is_element_present_now(selector),
            disappear_timeout,
            "the spinner to disappear",
        )

    def wait_for_stable(
        self,
        reader,
        timeout: float = SETTLE_TIMEOUT_S,
        description: str = "content",
        dwell: float = STABLE_DWELL_S,
    ) -> bool:
        """Wait until successive reads stay unchanged for at least `dwell` seconds.

        Comparing two back-to-back reads is not enough: both can land inside the same
        short-lived intermediate state and report it as settled.
        """
        state = {"value": reader(), "since": time.monotonic()}

        def is_stable():
            current = reader()
            now = time.monotonic()
            if current != state["value"]:
                state["value"], state["since"] = current, now
                return False
            return now - state["since"] >= dwell

        return self.wait_until(is_stable, timeout, f"{description} to stop changing")

    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll to the specified element on the page.
        Args:
            selector (str): CSS selector, XPath, or Playwright text selector.
        """
        self.logger.debug(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()
        self.logger.debug(f"Scrolled to element")
