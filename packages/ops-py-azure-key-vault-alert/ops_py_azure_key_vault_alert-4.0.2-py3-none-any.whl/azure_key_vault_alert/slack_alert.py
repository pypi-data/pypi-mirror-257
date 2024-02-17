#!/usr/bin/env python

import logging


def slack_alert(title, kv, max_chars=3500, slack_app=False, stdout_only=False, msg_handler=None):
    """Get the reports from the azure_key_vault_report object and push the reports to the msg_handler,
    or optionally just print to standard out.


    Parameters
    ----------
    title : str
        The title of the message
    kv : __init__.py
        An azure_key_vault_report object
    max_chars : int
        The value on which the payload / report is split on. Slack App will handle max 4000 chars
        Slack Workflow might be able to handle more, but both are set to default to 3500.
        Each chunk will then max be 3500 chars for each post.
    slack_app : bool
        Creates Slack APP payload(s) if set to True, else it will build payload(s) for Slack WORKFLOW
    stdout_only : bool
        If True the reports will only be printed to standard output instead of sent to the Message Handler.
    msg_handler : __init__.py
        A message_handler object
    Returns
    -------
    True
        If response from the POST has return code 200
    """

    # Get full report, including the top summary
    report = kv.get_markdown_report()

    # Return if no report
    if not isinstance(report, str):
        logging.warning("No report")
        return

    # If stdout_only the report is printed to standard output only and then return
    if stdout_only or not msg_handler:
        print(title)
        print(report)
        return

    # Initialize the success_counter. If one or more messages are posted this value will increase and be True
    success_counter = 0

    ##############################################################
    # SLACK APP
    ##############################################################
    # If posting to a Slack app the payload is created accordingly
    if slack_app:
        logging.info("Building payload for Slack App..")
        payloads = [{"text": f"*{title}*\n```{report}```"}]

        # If the payload is too large for the Slack App it will be split into multiple posts
        if len(str(payloads)) > max_chars:
            logging.info("The message will be to large. Splitting up into chunks..")
            payloads = split_msg(title, kv, max_chars, slack_app=slack_app)

        logging.info(f"{len(payloads)} payloads will be posted..")
        for p in payloads:
            msg_handler.set_payload(p)
            msg_handler.post_payload()

            # If any of the payloads are sent it is considered a success
            response_code = msg_handler.get_response_code()
            if isinstance(response_code, int) and response_code == 200:
                success_counter += 1
            else:
                logging.error(f"Failed to send message to Slack App. Response code {str(response_code)}.")

        # Return True if success so that we know at least one message have been sent
        if success_counter:
            logging.info(f"{success_counter} messages posted to the Slack app.")
            return True

        return

    ##############################################################
    # SLACK WORKFLOW
    ##############################################################
    # If posting to a Slack Workflow the payload is build by the Message Handler
    logging.info("Building payload for Slack Workflow..")
    posts = [(title, report)]

    # If the payload is too large for the Slack App it will be split into multiple posts
    if len(report) > max_chars:
        logging.info("The message will be to large. Splitting up into chunks..")
        posts = split_msg(title, kv, max_chars, slack_app=slack_app)

    logging.info(f"{len(posts)} post will be posted..")
    for title_, text_ in posts:
        msg_handler.build_payload(Title=title_, Text=text_)
        msg_handler.post_payload()

        # If any of the payloads are sent it is considered a success
        response_code = msg_handler.get_response_code()
        if isinstance(response_code, int) and response_code == 200:
            success_counter += 1
        else:
            logging.error(f"Failed to send message to Slack Workflow. Response code {str(response_code)}.")

    # Return True if success so that we know at least one message have been sent
    if success_counter:
        logging.info(f"{success_counter} messages posted to the Slack Workflow.")
        return True


def split_msg(title, kv, max_chars, slack_app=False):
    """Get the reports from the azure_key_vault_report object and push the reports to the msg_handler,
    or optionally just print to standard out.


    Parameters
    ----------
    title : str
        The title of the message
    kv : __init__.py
        An azure_key_vault_report object
    max_chars : int
        The value on which the payload / report is split on. Slack App will handle max 4000 chars
        Slack Workflow might be able to handle more, but both are set to default to 3500.
        Each chunk will then max be 3500 chars for each post.
    slack_app : bool
        Creates Slack APP payload(s) if set to True, else it will build payload(s) for Slack WORKFLOW
    Returns
    -------
    Results
        A list of payloads (Slack App) or a list of tuples (title, message)
    """
    results = []

    # If Slack App then the messages have to be formatted. Triple backticks are added in the beginning and in the
    # end of each message. If Slack Workflow, the formatting is handled by the Slack Workflow itself.
    # For Slack App 'payloads' are created. For Slack Workflow 'txt' items are created.
    cb = ""
    if slack_app:
        cb = "```"

    # The summary payload is created first and added to the list of results (to be posted)
    summary = kv.get_markdown_summary()
    if slack_app:
        payload = {"text": f"*{title} - summary*\n{cb}{summary}{cb}"}
        results.append(payload)
    else:
        results.append((f"{title} - summary", summary))

    # Then the report is split into chucks
    report = kv.get_markdown_report_only()
    report_lines = report.splitlines()

    # The two first lines of the report is the header, which will be used in every part
    header = f"{cb}{report_lines.pop(0)}\n{report_lines.pop(0)}\n"

    # The first part of the first report payload / txt is initialized
    part = 1
    txt = ""
    payload = {"text": f"*{title} - Part {part}*\n{header}"}

    # Parse through every line of data in the report and add it to individual payloads / txt
    for line in report_lines:
        if len(txt) <= max_chars:
            txt += f"{line}\n"
            payload["text"] += f"{line}\n"
        else:
            # When a payload / txt have reacted it's max size it is added to the list of results
            if slack_app:
                payload["text"] += cb
                results.append(payload)
            else:
                results.append((f"{title} - Part {part}", f"{header}{txt}"))

            # Then a new payload / txt is initialized
            part += 1
            txt = f"{line}\n"
            payload = {"text": f"*{title} - Part {part}*\n{header}{txt}"}

    # If a remaining payload / txt exists, then it will also be added to the list of payloads
    if txt:
        if slack_app:
            payload["text"] += cb
            results.append(payload)
        else:
            results.append((f"{title} - Part {part}", f"{header}{txt}"))

    logging.info(f"Message was split into {len(results)} chunks.")

    return results
