from google.cloud import vision

def func(path):
	client = vision.ImageAnnotatorClient()
	with open(path, 'rb') as image_file:
		content = image_file.read()
	image = vision.types.Image(content=content)

	objects = client.object_localization(
	image=image).localized_object_annotations

	print('Number of objects found: {}'.format(len(objects)))
	for object_ in objects:
		print(object_.name)
		'''
		print('\n{} (confidence: {})'.format(object_.name, object_.score))
		print('Normalized bounding polygon vertices: ')
		for vertex in object_.bounding_poly.normalized_vertices:
			print(' - ({}, {})'.format(vertex.x, vertex.y))

	print("*********************************\n")
	
	response = client.label_detection(image=image)
	labels = response.label_annotations
	ingredients = []
	for label in labels:
		ingredients.append(label.description)
	print(labels[0:5])
	'''
	
	