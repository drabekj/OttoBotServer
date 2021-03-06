# AddStockToWatchlistIntent
from app import ResponseBuilder, logger
from app.intent_watchlist.remove import _check_valid_ticker_provided
from app.models import Watchlist
from app.utils.MyError import EntryExistsError
from app.utils.authentication import authenticated
from static import strings


@authenticated
def handle_add_to_watchlist(request):
    """
    Generate response to intent type AddStockToWatchlistIntent based on the stage of the adding stock to portfolio process.
    :type request AlexaRequest
    :return: JSON response including appropriate response based on the stage in the adding process.
    """

    if request.dialog_state() == "STARTED":
        return _handle_dialog_add_started(request)
    elif request.dialog_state() == "IN_PROGRESS":
        return _handle_dialog_add_in_progress(request)
    elif request.dialog_state() == "COMPLETED":
        # TODO
        return ResponseBuilder.create_response(request, "Add to watchlist dialog completed! ")
    elif request.dialog_state() == "":
        # TODO
        print("LOG-d: dialogState not included")
        return ResponseBuilder.create_response(request, "Add to watchlist dialog state empty! ")
    else:
        print("LOG-d: dialogState else")
        # TODO
        print("LOG-d: dialogState not included")
        return ResponseBuilder.create_response(request, "Add to watchlist dialog state ELSE! ")


def _handle_dialog_add_started(request):
    """
    Check if the provided ticker is supported or is not already in watchlist, if not, ask for confirmation.
    :type request AlexaRequest
    """
    print("LOG-d: dialogState STARTED")

    # Check if ticker is provided
    try:
        ticker = _check_valid_ticker_provided(request)
    except AttributeError as e:
        logger.exception("No valid ticker provided")
        message = strings.INTENT_ADDED_TO_WATCHLIST_FAIL
        return ResponseBuilder.create_response(request, message=message) \
            .with_reprompt(strings.INTENT_GENERAL_REPROMPT)

    # Ask user to confirm ticker add
    message = strings.INTENT_ADD_TO_WATCHLIST_ASK_CONFIRMATION.format(ticker)

    # Check if ticker not already in Watchlist
    user_id = request.get_user_id()
    watchlist_tickers = Watchlist.get_users_tickers(user_id)
    for ticker_in_watchlist in watchlist_tickers:
        if ticker == ticker_in_watchlist:
            message = strings.INTENT_ADDED_TO_WATCHLIST_EXISTS.format(ticker)

    return ResponseBuilder.create_response(request, message) \
        .with_dialog_confirm_intent()


def _handle_dialog_add_in_progress(request):
    """
    Check if the stock adding request was confirmed by the user. If it was, add it to portfolio, otherwise do not add.
    :type request AlexaRequest
    """
    logger.debug("dialogState IN_PROGRESS")

    if request.get_intent_confirmation_status() == "CONFIRMED":
        return _add_ticker_to_watchlist(request)
    else:
        message = strings.INTENT_ADD_TO_WATCHLIST_DENIED
        return ResponseBuilder.create_response(request, message=message)


def _add_ticker_to_watchlist(request):
    """
    Add ticker to users Watchlist and build response.
    :type request AlexaRequest
    """
    user_id = request.get_user_id()
    ticker = request.get_slot_value('stockTicker')
    if ticker is None:
        ticker = request.get_session_attribute('stockTicker')

    message = strings.INTENT_ADD_TO_WATCHLIST_CONFIRMED.format(ticker)
    reprompt_message = strings.INTENT_GENERAL_REPROMPT

    # Save stock to watchlist
    try:
        user_id = request.get_user_id()
        Watchlist(ticker, user_id).save()
    except EntryExistsError as e:
        message = strings.ERROR_CANT_ADD_TO_WATCHLIST.format(ticker)

    return ResponseBuilder.create_response(request, message=message) \
        .with_reprompt(reprompt_message)