import ipih

from pih import A, PIHThread
from MessageReceiverService.const import SD

# version 1.2
SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    if A.U.for_service(SD, as_standalone=as_standalone):

        from pih.tools import j, js, ne, e, nl, esc
        from MessageReceiverService.collection import WappiRawMessage
        from pih.collections import WhatsAppMessage, BarcodeInformation

        from fastapi import FastAPI, Body, Request
        from fastapi.responses import HTMLResponse
        import uvicorn

        fast_api = FastAPI()

        @fast_api.get("/")
        def api_root():
            version: str = A.V.value
            return HTMLResponse(
                js((nl("Message app", normal=False), "Version:", version))
            )

        @fast_api.post("/message_gateway")
        def wappi_whatsapp_message_receive_handler(
            request: Request, message_body=Body(...)
        ):
            wh_type: str = message_body["wh_type"]
            if wh_type == "incoming_message":
                type: str | None = A.D.if_is_in(message_body, "type")
                if ne(type):
                    is_image: bool = type == "image"
                    is_chat: bool = type == "chat"
                    if is_chat or is_image:
                        raw_message: WappiRawMessage = A.D.fill_data_from_source(
                            WappiRawMessage(), message_body
                        )
                        raw_message.sender = message_body["from"]
                        raw_message.recipient = message_body["to"]
                        message: WhatsAppMessage = A.D.fill_data_from_source(
                            WhatsAppMessage(), raw_message.__dict__
                        )
                        message.message = (
                            A.D.if_is_in(message_body, "caption", "")
                            if is_image
                            else raw_message.body
                        )
                        recipient_telephone_number: str = A.D_Ex.wappi_telephone_number(
                            raw_message.recipient
                        )
                        sender_telephone_number: str = A.D_Ex.wappi_telephone_number(
                            raw_message.sender
                        )
                        message.from_me = A.C_ME_WH_W.from_me(sender_telephone_number)
                        message.recipient = recipient_telephone_number
                        message.sender = sender_telephone_number
                        if raw_message.chatId == raw_message.sender:
                            message.chatId = None
                        if is_image:
                            if message.profile_id == A.D.get(A.CT_ME_WH_W.Profiles.IT):
                                wait_for_input_polibase_person_pin: bool = A.IW.has(
                                    A.CT_P.NAMES.PERSON_PIN,
                                    sender_telephone_number,
                                )
                                image_path: str = A.PTH.join(
                                    A.PTH.MOBILE_HELPER.INCOME_IMAGES_FOLDER,
                                    A.PTH.add_extension(A.D.uuid(), A.CT_F_E.JPG),
                                )
                                A.D.save_base64_as_image(image_path, raw_message.body)
                                barcode_information_list: (
                                    list[list[BarcodeInformation]] | None
                                ) = A.R_RCG.barcodes_information(
                                    image_path, True, 0
                                ).data
                                if (
                                    ne(barcode_information_list)
                                    and ne(barcode_information_list[0])
                                    and A.D_C.polibase_person_barcode(
                                        barcode_information_list[0][0]
                                    )
                                ):
                                    barcode_information: BarcodeInformation = (
                                        barcode_information_list[0][0]
                                    )
                                    if ne(barcode_information.data):
                                        if wait_for_input_polibase_person_pin:
                                            message.message = barcode_information.data
                                        else:
                                            if e(message.message):
                                                message.message = js(
                                                    (
                                                        A.root.NAME,
                                                        "card",
                                                        "registry",
                                                        "find",
                                                        barcode_information.data,
                                                    )
                                                )
                                            else:
                                                message.message = js(
                                                    (
                                                        A.root.NAME,
                                                        "card",
                                                        "registry",
                                                        message.message,
                                                        barcode_information.data,
                                                    )
                                                )
                                else:
                                    if wait_for_input_polibase_person_pin:
                                        message.message = A.CT_P.BARCODE.NOT_FOUND
                                    else:
                                        if ne(message.message):
                                            message.message += " "
                                        message.message = j(
                                            (message.message, esc(image_path))
                                        )
                        else:
                            wait_for_input_polibase_person_card_registry_folder: (
                                bool
                            ) = A.IW.has(
                                A.CT_P.NAMES.PERSON_CARD_REGISTRY_FOLDER,
                                sender_telephone_number,
                            )
                            if wait_for_input_polibase_person_card_registry_folder:
                                message_parts: list[str] = A.D.not_empty_items(
                                    message.message.lower().strip().split(" ")
                                )
                                if len(message_parts) == 4:
                                    for part in [A.root.NAME, "card", "registry"]:
                                        if part in message_parts:
                                            message_parts.remove(part)
                                    if len(
                                        message_parts
                                    ) == 1 and A.C_P.person_card_registry_folder(
                                        message_parts[0]
                                    ):
                                        message.message = message_parts[0]
                        A.E.whatsapp_message_received(message)

        def service_starts_handler() -> None:
            A.SYS.kill_process_by_port(A.CT_PORT.HTTP)
            PIHThread(run_fastapi_server)

        def run_fastapi_server() -> None:
            uvicorn.run(fast_api, host="0.0.0.0", port=A.CT_PORT.HTTP)

        A.SRV_A.serve(
            SD,
            starts_handler=service_starts_handler, # type: ignore
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
