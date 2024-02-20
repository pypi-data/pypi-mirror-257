import pygame
from .TextBox import TextBox


class FloatBox(TextBox):
    def __init__(
        self, 
        x: int=0, 
        y:int=0, 
        width: int=100, 
        height: int=40, 
        standard_value: float=0,
        font: str='FreeSans.ttf',
        font_size: int=20,
        box_color: tuple[int]=(200, 200, 200),
        border: bool=True,
        border_color: tuple[int]=(70, 70, 70),
        border_radius: int=3,
        text_color: tuple[int]=(70, 70, 70),
        selected_text_color: tuple[int]=(0, 0, 0),
        selected_color: tuple[int]=(220, 255, 255),
        name = "", 
        name_color: str= (0, 0, 0),
        replace_text: bool = True
        ) -> None:
        """Generates a floatbox. the saved value can be returned using floatbox.get_value()

        Args:
            x (int, optional): the x position of the floatbox. Defaults to 0.
            y (int, optional): the y position of the floatbox. Defaults to 0.
            width (int, optional): the width of the floatbox. Defaults to 120.
            height (int, optional): the height of the floatbox. Defaults to 30.
            standard_value (str, optional): the value the floatbox has when initialized. Defaults to "".
            font (str, optional): the font used for the text and name of the floatbox. Defaults to 'FreeSans.ttf'.
            font_size (int, optional): the size of the font. Defaults to 20.
            box_color (tuple[int], optional): the color of the floatbox. Defaults to (200, 200, 200).
            border (bool, optional): if True the floatbox will have a displayed border. Defaults to True.
            border_color (tuple[int], optional): the color of the border of the floatbox. Defaults to (70, 70, 70).
            border_radius (int, optional): smoothens the edge of the floatbox. Defaults to 3.
            text_color (tuple[int], optional): the color of the text within the floatbox if not selected. Defaults to (70, 70, 70).
            selected_text_color (tuple[int], optional): the color of the text within the floatbox when selected. Defaults to (0, 0, 0).
            selected_color (tuple[int], optional): the color of the floatbox when selected. Defaults to (220, 255, 255).
            name (str, optional): the name of the floatbox that will be displayed above the floatbox. Defaults to "".
            name_color (str, optional): the color of the name that will be displayed above the floatbox. Defaults to (0, 0, 0).
            replace_text (bool, optional): if True the value within the TextBox will be replaced, when selecting the TextBox. If nothing is entered the TextBox regains its old value.

        Raises:
            ValueError: a minimum height of 25 is required to be able to display the text correctly
            ValueError: if the given standard_value is not of type float
        """
        super().__init__(
            x=x, 
            y=y, 
            width=width, 
            height=height, 
            standard_value=standard_value, 
            font=font, 
            font_size=font_size, 
            box_color=box_color, 
            border=border, 
            border_color=border_color, 
            border_radius=border_radius, 
            text_color=text_color, 
            selected_text_color=selected_text_color, 
            selected_color=selected_color, 
            name=name, 
            name_color=name_color,
            replace_text=replace_text
        )
        try:
            float(standard_value)
        except:
            raise ValueError(f"{standard_value} is not a float")
        
        
    def get_value(self) -> float:
        """This method returns the value within the floatbox

        Returns:
            float: the saved value within the floatbox
        """
        return self._saved_val
    
        
    def draw(self, surface: pygame.Surface) -> None:
        """This method displays the floatbox on a given pygame surface

        Args:
            surface (pygame.Surface): the surface the floatbox will be displayed on
        """
        super().draw(surface)


    def handleEvent(self, event: pygame.event.Event) -> None:
        """Eventhandler for pygame events makes the floatbox accessable

        Args:
            event (pygame.event.Event): makes the floatbox accessable
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._fgRect.collidepoint(event.pos):
                self._selected = not self._selected
                
                # handling text replacement
                if self._replace_text:
                    self._value = ""
            else:
                # save the value if clicked outside of the FloatBox
                self._selected = False
                try:
                    self._saved_val = float(self._value) if self._value.strip() != "" else self._saved_val
                    self._st_val = self._saved_val
                except:
                    self._saved_val = self._st_val
                self._value = str(self._saved_val)

        if event.type == pygame.KEYDOWN:
            if self._selected:
                if event.key == pygame.K_RETURN:
                    # save the value if the Enter key is pressed
                    try:
                        self._saved_val = float(self._value) if self._value.strip() != "" else self._saved_val
                        self._st_val = self._saved_val
                    except:
                        self._saved_val = self._st_val
                    self._value = str(self._saved_val)
                
                # handling key inputs (backspace and letters)
                elif event.key == pygame.K_BACKSPACE:
                    self._value = self._value[:-1]
                elif self._text.get_width() < self._width - 10 and event.unicode.isnumeric() or event.unicode == ".":
                    self._value += event.unicode


        # setting the color of the text inside the TextBox
        text_color = self._text_color if not self._selected else self._selected_text_color
        
        # text to be displayed inside the TextBox
        txt = self._value if self._selected else self._saved_val
        self._text = self._font.render(str(txt), True, text_color)
        
        # setting the color of the box
        self._current_box_color = self._selected_color if self._selected else self._box_color