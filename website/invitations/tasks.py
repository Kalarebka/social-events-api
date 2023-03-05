# # tasks.py
# from celery import shared_task
# from django.core.mail import send_mail
# from django.template.loader import render_to_string


# @shared_task
# def send_invitation_email(invitation_id):
#     invitation = AbstractInvitation.objects.get(pk=invitation_id)
#     subject, message, from_email, recipient_list = invitation.get_email_data()
#     send_mail(subject, message, from_email, recipient_list, fail_silently=False)


# @shared_task
# def send_many_invitation_emails(invitation_ids):
#     invitations = AbstractInvitation.objects.filter(pk__in=invitation_ids)
#     email_messages = []
#     for invitation in invitations:
#         subject, message, from_email, recipient_list = invitation.get_email_data()
#         email_messages.append((subject, message, from_email, recipient_list))
#     send_mail(email_messages, fail_silently=False)


# # views.py
# from django.shortcuts import render
# from .tasks import send_invitation_email, send_many_invitation_emails

# def create_invitation(request):
#     # Code to create an invitation object
#     invitation = GroupInvitation(sender=sender, receiver=receiver, group=group)
#     invitation.save()

#     # Call the send_invitation_email task for one invitation
#     send_invitation_email.delay(invitation.pk)

#     # Call the send_many_invitation_emails task for a list of invitations
#     invitation_ids = [invitation.pk for invitation in invitations]
#     send_many_invitation_emails.delay(invitation_ids)

#     # Render the response
#     return render(request, 'create_invitation.html', {'invitation': invitation})
