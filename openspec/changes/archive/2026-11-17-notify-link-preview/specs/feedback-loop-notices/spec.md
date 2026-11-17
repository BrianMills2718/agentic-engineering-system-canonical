## ADDED Requirements

### Requirement: A caller can turn off the link preview

`notify.py` `push()` SHALL accept `no_preview`; when it is true the `sendMessage` body SHALL carry
`disable_web_page_preview: true`, and when it is false (the default) the body SHALL be unchanged. A delivered result
SHALL also carry the `message_id`. An HTTP error result SHALL carry Telegram's `description` with the token removed.

Source: inferred by agent, from the AES consolidation plan row 11 (the waiting-issue push moves off Project Meta's
`deliver_telegram`, which sent the same flag).

#### Scenario: link-preview-off-on-request

- **WHEN** `push()` is called with `no_preview=True` and Telegram accepts the message
- **THEN** the body is the chat id, the text and `disable_web_page_preview: true`, and the result carries the message id
- **AND WHEN** Telegram answers an HTTP error with a description
- **THEN** the result is not delivered, carries the description and does not carry the token
