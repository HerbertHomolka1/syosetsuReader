import os

# Get the home directory
home_directory = os.path.expanduser("~")

# Define the file path within the .local directory
file_path = os.path.join(home_directory,'.local', "share", "Anki2","User 1","61Srea33333333333dme.txt")

# Write to the file
with open(file_path, 'w') as f:
    f.write('readme')



# from anki.storage import Collection

# notes = [ 
#   {
#     "Front": "Bonjour",
#     "Back": "Hello",
#   },
#   {
#     "Front": "Merci",
#     "Back": "Thank you",
#   },
#   # Thousands of additional notes...
# ]

# # Find the Anki directory
# anki_home = '/.local/share/Anki2/User 1/'
# anki_collection_path = os.path.join(anki_home, "collection.anki2")

# # 1. Load the anki collection
# col = Collection(anki_collection_path)

# # 2. Select the deck
# modelBasic = col.models.byName('Basic')
# deck = col.decks.byName('Default')
# col.decks.select(deck['id'])
# col.decks.current()['mid'] = modelBasic['id']

# # 3. Create the cards
# for current_note in notes: 
#   note = col.newNote()
#   note.fields[0] = current_note["Front"]
#   note.fields[1] = current_note["Back"]
#   col.add_note(note, deck['id'])

# # 4. Save changes
# col.save()