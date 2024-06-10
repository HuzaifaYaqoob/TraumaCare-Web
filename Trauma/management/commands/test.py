



from django.core.management.base import BaseCommand

import csv

from ChatXpo.Sockets.Constant.Query import askChatXpo

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        chats = []
        while True:
            msg = input('Huzaifa : ')
            
            response = askChatXpo(msg, previousQueries=chats)

            answer = response
            print(f'ChatXpo : {answer}')
            chats.append(
                {
                    'role' : 'assistant',
                    'content' : answer
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

