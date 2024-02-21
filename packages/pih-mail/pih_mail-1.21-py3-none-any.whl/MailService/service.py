import ipih

from pih import A
from pih.tools import ne, j, n, e
from MailService.const import *
from pih.collections import MailboxInfo, NewMailMessage

from time import sleep
from typing import Any
# version 1.0

SC = A.CT_SC
EVM = A.CT_EVM

ISOLATED: bool = False

class DH:
    EMAIL_IT_USER_PASSWORD: str | None = None
    EXTERNAL_EMAIL_USER_PASSWORD: str | None = None
    EMAIL_ADD_EMAIL_USER_PASSWORD: str | None = None
    ABSTRACT_API_KEY: str | None = None


def start(as_standalone: bool = False) -> None:
    
    if A.U.for_service(SD, as_standalone=as_standalone):
        
        from pih.tools import ParameterList
       
        from imap_tools.mailbox import MailMessage
        from imap_tools import MailBox, AND
        from requests import Response
        from smtplib import SMTP
        import requests
        import ssl

        def service_call_handler(sc: SC, pl: ParameterList) -> Any | None:
            if sc == SC.heart_beat:
                for mailbox_item in [
                    (A.CT_ADDR.EMAIL_SERVER_ADDRESS, A.CT_EML.IT, DH.EMAIL_IT_USER_PASSWORD),
                    (A.CT_ADDR.EMAIL_SERVER_ADDRESS, A.CT_EML.ADD_EMAIL, DH.EMAIL_ADD_EMAIL_USER_PASSWORD),
                    (
                        A.CT_EML.EXTERNAL_SERVER,
                        A.CT_EML.EXTERNAL,
                        DH.EXTERNAL_EMAIL_USER_PASSWORD,
                    ),
                ]:
                    try:
                        mailbox_server: str = mailbox_item[0]
                        mailbox_address: str = mailbox_item[1]
                        mailbox_password: str = mailbox_item[2]
                        mail_message: MailMessage | None = None
                        with MailBox(mailbox_server).login(
                            mailbox_address, mailbox_password
                        ) as mailbox:
                            mail_message_list: list[MailMessage] = []
                            mailbox_info: MailboxInfo | None = A.R.get_first_item(
                                A.R_DS.value(mailbox_address, A.D_Ex.mailbox_info, SECTION)
                            )
                            last_uid: str | None = None
                            if ne(mailbox_info):
                                last_uid = mailbox_info.last_uid
                            for mail_message in mailbox.fetch(
                                AND(date=A.D.today()),
                                mark_seen=False,
                                headers_only=True,
                                bulk=True,
                            ):
                                if e(last_uid) or (
                                    ne(mail_message.uid)
                                    and int(last_uid) < int(mail_message.uid)
                                ):
                                    mail_message_list.append(mail_message)
                            if ne(mail_message_list):
                                new_mail_messages: list[NewMailMessage] = []
                                for mail_message in mailbox.fetch(
                                    AND(
                                        uid=list(
                                            map(lambda item: item.uid, mail_message_list)
                                        )
                                    )
                                ):
                                    new_mail_message: NewMailMessage = NewMailMessage(
                                        mailbox_address,
                                        mail_message.subject,
                                        mail_message.text,
                                        mail_message.from_,
                                    )
                                    new_mail_messages.append(new_mail_message)
                                    A.E.new_mail_message_was_received(new_mail_message)
                                mail_message = mail_message_list[-1]
                                A.A_DS.value(
                                    MailboxInfo(mail_message.date, mail_message.uid),
                                    mailbox_address,
                                    SECTION,
                                )
                    except Exception as _:
                        pass
                return True
            if sc == SC.check_email_accessibility or sc == SC.get_email_information:
                email_address: str = pl.next()
                content: dict[str, Any] | None = None
                count: int = TRY_AGAIN_COUNT
                while True:
                    try:
                        response: Response = requests.get(
                            j(
                                (
                                    "https://emailvalidation.abstractapi.com/v1/?api_key=",
                                    DH.ABSTRACT_API_KEY,
                                    "&email=",
                                    email_address,
                                )
                            ),
                            timeout=TIMEOUT,
                        )
                        if response.status_code == 200:
                            content = A.D.rpc_unrepresent(response.content.decode("utf-8"))
                            break
                        else:
                            sleep(TRY_AGAIN_SLEEP_TIME)
                            if count == 0:
                                break
                            count -= 1
                    except Exception as _:
                        sleep(TRY_AGAIN_SLEEP_TIME)
                        if count == 0:
                            break
                        count -= 1
                if sc == SC.check_email_accessibility:
                    if n(content):
                        return None
                    return content["deliverability"] == "DELIVERABLE"
                return A.R.pack(A.CT_FC.VALUE, content)

            if sc == SC.send_email:
                context = ssl.create_default_context()
                server: SMTP = SMTP(A.CT_ADDR.EMAIL_SERVER_ADDRESS, A.CT_PORT.SMTP)
                try:
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(A.CT_EML.IT, DH.EMAIL_IT_USER_PASSWORD)
                    server.sendmail(
                        A.CT_EML.IT,
                        pl.next(),
                        pl.next().encode("utf-8"),
                    )
                except Exception as _:
                    pass
                finally:
                    server.quit()

            return False

        def service_starts_handler() -> None:
            DH.EMAIL_IT_USER_PASSWORD = A.D_V_E.value("EMAIL_IT_USER_PASSWORD")
            DH.EXTERNAL_EMAIL_USER_PASSWORD = A.D_V_E.value("EXTERNAL_EMAIL_USER_PASSWORD")
            DH.EMAIL_ADD_EMAIL_USER_PASSWORD = A.D_V_E.value("EMAIL_ADD_EMAIL_USER_PASSWORD")
            DH.ABSTRACT_API_KEY = A.D_V_E.value("ABSTRACT_API_KEY")
            A.SRV_A.subscribe_on(SC.heart_beat)

        A.SRV_A.serve(SD, service_call_handler, service_starts_handler, isolate=ISOLATED, as_standalone=as_standalone, max_workers=1)
        
if __name__ == "__main__":
    start()
