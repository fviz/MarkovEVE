import markovify

# Get raw text as a string
with open("text.txt") as f:
	text = f.read()

# Build the model
text_model = markovify.Text(text)

# Print five randomly-generated sentences
print("Random sentences:")
for i in range(5):
	print(text_model.make_sentence())
print("\n")

# Print three random-ly generated sentences of no more than 140 characters
print("Random sentences (max. 140 characters):")
for i in range(3):
	print(text_model.make_short_sentence(140))
