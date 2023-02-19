from django.template.loader import render_to_string
from django.core.mail import send_mail


def send_invitation_email_task(sender, receiver, invite_to, template=None):
    # if not template use default template
    # maybe do a default template variable in django settings?
    # read the template from file
    # something along the lines of:
    # email_template = "path to template.html"
    # confirmation_url = "url to GET endpoint to confirm the invitation"
    # email_content = render_to_string(
    #     email_template,
    #     {
    #         "invite_to": invite_to,
    #         "sender_username": sender.username,
    #         "confirmation_url": confirmation_url,
    #     },
    # )
    # send_mail(
    #     "You've received an invitation on Events App",
    #     email_content,
    #     "from_email?",
    #     [receiver.email],
    # )
    # + whatever else the email sending function needs
    #
    pass


# There should also be a version to send_mass_mail when inviting a list of users (all friends or all
# group members for a group event invitation)
# or maybe just override the save in event_invitation model to send a batch of emails? friend and
# group invitations can stay separate
