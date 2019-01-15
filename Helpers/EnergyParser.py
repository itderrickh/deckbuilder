def parse_energy(string_contents, sets):
	#sets = ses.query(CardSet.name).all()
	array_contents = string_contents.split()
	count_of_card = array_contents[0] # Guaranteed information
	length_of_contents = len(array_contents)

	energy_name = ""
	set_number = ""
	set_name = ""
	word = ""
	iterator = 1
	while(word.lower() != "energy"):
		# Sanity check for energy name
		if iterator >= length_of_contents:
			return count_of_card, energy_name + " Energy", set_name, set_number
		word = array_contents[iterator]
		energy_name += word

		if word.lower() != "energy":
			energy_name += " "
		iterator += 1

	if iterator != length_of_contents:
		# Process the rest of the information
		remaining_elements = array_contents[iterator:length_of_contents]
		set_number_list = [item for item in remaining_elements if item.isdigit()]
		set_name_list = [item for item in remaining_elements if item in sets]

		set_number = set_number_list[0] if len(set_number_list) > 0 else ""
		set_name = set_name_list[0] if len(set_name_list) > 0 else ""

		if len(set_name) > 0:
			remaining_elements.remove(set_name)
		if len(set_number) > 0:
			remaining_elements.remove(set_number)

		# If there is no set number, the rest has to be additonal parameters
		if len(remaining_elements):
			energy_name += " " + " ".join(remaining_elements)

	return count_of_card, energy_name, set_name, set_number