from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="AI_MENTOR",
    environment=True,
    settings_files=["settings.toml"],
    load_dotenv=True,
    env_switcher="SERVICE_ENV",
    dotenv_path="../.env",
)

base_prompt = """
            Напиши .tsx код для этой страницы(главное - сохранить описанную структуру UI и адаптивность), 
            важно: absolute позиционирование нельзя включать в стили, оно нужно только чтобы через положение X и Y показать расположение элементов друг от друга.
            Исходя из координат элементов - организовать адаптивную html структуру с heroui компонентами:
            <flex>
                dir:column
                justify:start
                align:stretch
                spacing:0
                padding:0
                width:1440
                height:900
                x:0
                y:0
                    <!-- Верхняя панель управления (Toolbar) -->
                    <flex>
                    dir:row
                    justify:between
                    align:center
                    spacing:20
                    padding:10
                    width:1440
                    height:50
                    x:-
                    y:-
                        <flex>
                        dir:row
                        justify:start
                        align:center
                        spacing:15
                        padding:0
                        width:300
                        height:40
                        x:-
                        y:-
                            <widget>
                            type:Button
                            content:"Файл"
                            notes:"Выпадающее меню управления проектом"
                            width:60
                            height:30
                            x:-
                            y:-
                            </widget>
                            <widget>
                            type:Button
                            content:"Экспорт"
                            notes:"Кнопка рендеринга видео"
                            width:80
                            height:30
                            x:-
                            y:-
                            </widget>
                        </flex>
                        <widget>
                        type:Label
                        content:"Project_Final_v2.mp4"
                        notes:"Название текущего проекта"
                        width:200
                        height:30
                        x:-
                        y:-
                        </widget>
                        <widget>
                        type:Avatar
                        content:"AI"
                        notes:"Профиль пользователя"
                        width:35
                        height:35
                        x:-
                        y:-
                        </widget>
                    </flex>

                    <!-- Основная рабочая зона -->
                    <flex>
                    dir:row
                    justify:start
                    align:stretch
                    spacing:2
                    padding:0
                    width:1440
                    height:550
                    x:-
                    y:-
                        <!-- Левая панель: Ресурсы и Эффекты -->
                        <flex>
                        dir:column
                        justify:start
                        align:stretch
                        spacing:10
                        padding:10
                        width:300
                        height:550
                        x:-
                        y:-
                            <widget>
                            type:Tabs
                            content:"Медиа, Эффекты, Переходы"
                            notes:"Переключение между библиотекой файлов и списком фильтров"
                            width:280
                            height:40
                            x:-


y:-
                            </widget>
                            <widget>
                            type:ScrollArea
                            content:"Список видео-клипов"
                            notes:"Сетка с превью загруженных видео и аудио файлов"
                            width:280
                            height:480
                            x:-
                            y:-
                            </widget>
                        </flex>

                        <!-- Центральная панель: Превью -->
                        <flex>
                        dir:column
                        justify:center
                        align:center
                        spacing:15
                        padding:20
                        width:840
                        height:550
                        x:-
                        y:-
                            <widget>
                            type:VideoPlayer
                            content:"Preview Window"
                            notes:"Окно предпросмотра видео с контроллами воспроизведения"
                            width:800
                            height:450
                            x:-
                            y:-
                            </widget>
                            <flex>
                            dir:row
                            justify:center
                            align:center
                            spacing:20
                            padding:0
                            width:400
                            height:40
                            x:-
                            y:-
                                <widget>type:Button content:"⏮" notes:"Step back" width:40 height:30 x:- y:- </widget>
                                <widget>type:Button content:"▶" notes:"Play/Pause" width:50 height:40 x:- y:- </widget>
                                <widget>type:Button content:"⏭" notes:"Step forward" width:40 height:30 x:- y:- </widget>
                            </flex>
                        </flex>

                        <!-- Правая панель: Инспектор свойств -->
                        <flex>
                        dir:column
                        justify:start
                        align:stretch
                        spacing:15
                        padding:15
                        width:300
                        height:550
                        x:-
                        y:-
                            <widget>
                            type:Label
                            content:"Свойства клипа"
                            notes:"Заголовок инспектора"
                            width:270
                            height:30
                            x:-
                            y:-
                            </widget>
                            <widget>
                            type:Slider
                            content:"Прозрачность"
                            notes:"Регулировка opacity выбранного элемента"
                            width:270
                            height:40
                            x:-
                            y:-
                            </widget>
                            <widget>
                            type:Select
                            content:"Режим наложения"
                            notes:"Dropdown: Screen, Multiply, Overlay"
                            width:270
                            height:40
                            x:-
                            y:-
                            </widget>
                            <widget>
                            type:ColorPicker
                            content:"Цветокоррекция"
                            notes:"Выбор цвета или tint для слоя"
                            width:270
                            height:150
                            x:-
                            y:-
                            </widget>
                        </flex>
                    </flex>


<!-- Нижняя панель: Таймлайн (Timeline) -->
                    <flex>
                    dir:column
                    justify:start
                    align:stretch
                    spacing:5
                    padding:10
                    width:1440
                    height:300
                    x:-
                    y:-
                        <flex>
                        dir:row
                        justify:between
                        align:center
                        spacing:0
                        padding:5
                        width:1420
                        height:40
                        x:-
                        y:-
                            <widget>
                            type:Label
                            content:"00:04:12:15"
                            notes:"Текущий таймкод"
                            width:150
                            height:30
                            x:-
                            y:-
                            </widget>
                            <widget>
                            type:Slider
                            content:"Zoom"
                            notes:"Масштаб таймлайна"
                            width:200
                            height:20
                            x:-
                            y:-
                            </widget>
                        </flex>
                        <widget>
                        type:TimelineEditor
                        content:"Слои видео и аудио"
                        notes:"Сложная область со слоями, где можно двигать блоки видео, обрезать их и накладывать звуковые дорожки"
                        width:1420
                        height:230
                        x:-
                        y:-
                        </widget>
                    </flex>
                </flex>
            Используй компоненты из HeroUI. Соблюдай структуру, padding и margin не больше 2.
"""