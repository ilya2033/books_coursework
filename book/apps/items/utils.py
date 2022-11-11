
from PIL import Image




order_by = ['Сначала новые','Сначала старые','По названию','Дате обновления']


norm_orders = {
	'Сначала новые':'item_date',
	'Сначала старые':'-item_date',
	'По названию':'item_title',
	'Дате обновления': "-last_upd",
}


#Получение ключа через значение
def get_dict_key(d, value):
    for k, v in d.items():
        if v == value:
            return k










#Обрезка изображения с ценрированием 
def crop_image(input_image_path,output_image_path,):
	img = Image.open(input_image_path)
	print(input_image_path)
	print(output_image_path)
	width, height = img.size
	if height>width:
		scale = height/5
		if width/scale!= 3:
			size = width-scale*3
			area = (size/2,0,size/2+scale*3,height)
		else:
			return 0
	elif width>height:
		scale = width/3
		if height/scale!= 5:
			size = height-scale*5
			area = (0,size/2,width,size/2+scale*5 )
		else:
			return 0
	else:
		return 0
	cropped_img = img.crop(area)
	cropped_img.save(output_image_path)