import flet
from flet import *
from location_details import get_location_details
from weather_details import Weaher_details


WINDOW_WIDTH = 412
WINDOW_HEIGHT = 732


weather_details = Weaher_details

def main(page:Page):
	page.horizontal_alignment = "center"
	page.vertical_alignment = "center"

	def _expand(e):
		_c.content.controls[0].height = WINDOW_HEIGHT * 0.8 if _c.content.controls[0].height == WINDOW_HEIGHT * 0.4 \
			else WINDOW_HEIGHT * 0.4
		_c.update()

	def _top():

		def get_location(e):
			localisation_data = get_location_details(new_location.value)
			if localisation_data == None:
				location_details.value =  "Error, cant find data about this location"
				page.update()
			if localisation_data:
				print(localisation_data)
				location_details.value = localisation_data[0]
				current_weather_details = weather_details(localisation_data).current_weather()
				print(current_weather_details)
				print("b")
				page.update()
			return localisation_data

		new_location = TextField(label="Location", width=250)
		location_details = Text()
		top = Container(
			width=WINDOW_WIDTH,
			height=WINDOW_HEIGHT * 0.4,
			gradient=LinearGradient(
				begin=alignment.bottom_left,
				end=alignment.top_right,
				colors=["blue", "orange"]
			),
			border_radius=35,
			animate=animation.Animation(700, AnimationCurve.EASE),
			on_hover=_expand,
			padding = 15,
			content=Column(
				alignment="start",
				spacing=10,
				controls=[
					Row(
						alignment='center',
						controls=[
							new_location,
							IconButton(on_click=get_location, icon=icons.SEARCH, icon_color="green",
									   icon_size=35, tooltip="Search", bgcolor="pink"
									   )
						],
					),
					Row(
						alignment="center",
						controls=[
							location_details
						]
					)
				]
			)
		)

		return top

	_c = Container(
		width=WINDOW_WIDTH,
		height=WINDOW_HEIGHT,
		border_radius=35,
		bgcolor="red",
		padding=10,
		content=Stack(
			width=WINDOW_WIDTH-20, height=WINDOW_HEIGHT-20,
			controls=[
				_top()
			]
		)
	)

	page.add(_c)



# https://open-meteo.com/en/docs#latitude=52.2298&longitude=21.0118&hourly=&daily=temperature_2m_max,temperature_2m_min

flet.app(target=main)