import reflex as rx
from sqlmodel import select

from rxconfig import config
from collections import Counter

from .model.user_model import Users

#class User(rx.Base):
    #login: str
    #user_name: str
    #email: str
    #gender: str

class State(rx.State):
    users: list[Users] = []
    current_user: Users = Users()

    users_for_graph: list[dict] = []

    #Función que carga los datos en la tabla
    def load_users(self) -> list[Users]:
        """Get all users from the database."""
        with rx.session() as session:
            query = select(Users)
            self.users = session.exec(query).all()

        self.transform_data()

    #Función que trae los datos de un usuario
    def get_user(self, user: Users):
        
        self.current_user = user
        #print(self.current_user)

    #Funcion que agrega objetos User a la lista "users"
    def add_user(self, form_data: dict):
        """Add users in the database."""

        with rx.session() as session:
            query = select(Users).where(Users.email == form_data['email'])
            user=session.exec(query).first()
                
            if user:
                return rx.toast.error('User with this email already exists', position="top-center",)
            
            session.add(
                Users(
                    login=form_data['login'],
                    user_name=form_data['user_name'],
                    email=form_data['email'],
                    gender=form_data['gender'],
                )
            )
            session.commit()
        #self.users.append(Users(**form_data))
        self.load_users()
        self.transform_data()
        return rx.toast.success(f"User {form_data['user_name']} has been added.", position="top-center",)

    def update_user(self, form_data: dict):
        with rx.session() as session:
            user = session.exec(select(Users).where(Users.id == self.current_user.id)).first()
            user.login=form_data['login'],
            user.user_name=form_data['user_name'],
            user.email=form_data['email'],
            user.gender=form_data['gender'],
            session.add(user)
            session.commit()
            session.refresh(user)
        self.load_users()
        self.transform_data()
        return rx.toast.success(f"User {user.user_name} has been update.", position="top-center",)

    
    def delete_user(self, id: int):
        """Delete a customer from the database."""
        with rx.session() as session:
            user = session.exec(select(Users).where(Users.id == id)).first()
            session.delete(user)
            session.commit()
        self.load_users()
        self.transform_data()
        return rx.toast.success(f"User {user.user_name} has been deleted.", position="top-center",)



    def transform_data(self):
        # Contar usuarios de cada grupo de género
        gender_counts = Counter(
            user.gender for user in self.users
        )

        # Transform into list of dict so it can be used in the graph
        self.users_for_graph = [
            {"name": gender_group, "value": count}
            for gender_group, count in gender_counts.items()
        ]



#función que muestra los usuarios en la tabla
def sow_user(user: Users):
    return rx.table.row(
        rx.table.cell(user.login),
        rx.table.cell(user.user_name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
        rx.table.cell(
            rx.hstack(
                edit_customer_button(user),
                rx.button(
                    rx.icon("trash", size=18),
                    color_scheme="tomato",
                    on_click=State.delete_user(user.id),
                ),
            ),
        ),
        style={
            "_hover": {"bg": rx.color("gray", 3)}
        },
        align="center",
    )

def add_customer_button():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add User", size="4"),
            ),
        ),

        rx.dialog.content(
            rx.dialog.title(
                "Add New User",
            ),

            rx.dialog.description(
                "Fill the form with the user's info",
            ),

            rx.form(
                rx.flex(
                    rx.input(
                        name="login",
                        placeholder="login",
                        type="text",
                        required=True,
                        spell_check=True,
                    ),

                    rx.input(
                        name="user_name",
                        placeholder="User Name",
                        type="text",
                        required=True,
                    ),

                    rx.input(
                        name="email",
                        placeholder="user@example.com",
                        type="email",
                        required=True,
                    ),

                    rx.select(
                        ["Male", "Female"],
                        name="gender",
                        placeholder="Select...",
                        required=True,
                    ),
                    
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Save",
                                type="submit",
                            ),
                        ),

                        spacing="3",
                        justify="end",
                    ),

                    direction="column",
                    spacing="4",
                ),

                on_submit=State.add_user,
                reset_on_submit=True,
            ),
            max_width="450px",
        ),
    )
        

def edit_customer_button(user: Users):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon(
                    "pencil", size=18,
                ),
                on_click=lambda: State.get_user(user),
                color_scheme="iris",
            ), 
        ),

        rx.dialog.content(
            rx.dialog.title(
                "Edit User",
            ),

            rx.dialog.description(
                "Update the form with the user's info",
            ),

            rx.form(
                    rx.flex(
                        rx.input(
                            name="login",
                            placeholder="login",
                            required=True,
                            default_value=user.login,
                        ),
                        
                        rx.input(
                            name="user_name",
                            placeholder="User Name",
                            required=True,
                            default_value=user.user_name,
                        ),

                        rx.input(
                            name="email",
                            #placeholder="user@example.com",
                            required=True,
                            default_value=user.email,
                        ),

                        rx.select(
                            ["Male", "Female"],
                            name="gender",
                            #placeholder="Select...",
                            required=True,
                            default_value=user.gender,
                        ),
                        
                        rx.flex(
                            rx.dialog.close(
                                rx.button(
                                    "Cancel",
                                    variant="soft",
                                    color_scheme="gray",
                                ),
                            ),
                            rx.dialog.close(
                                rx.button(
                                    "Save",
                                    type="submit",
                                ),
                            ),

                            spacing="3",
                            justify="end",
                        ),

                        direction="column",
                        spacing="4",
                    ),

                    on_submit=State.update_user,
                    reset_on_submit=False,
                ),
            max_width="450px",   
        )
    )


# Función que renderiza el grafico
def graph():
    return rx.vstack(
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="value",
                stroke=rx.color("accent", 9),
                fill=rx.color("accent", 8),
            ),

            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            data=State.users_for_graph,
            width="100%",
            height=250,
        ),
        width="25%",
        align="center",
        justify="center",
        padding="40px 0px"
    )



def index() -> rx.Component:
    return rx.vstack(
        # JavaScript único que se encarga de todo
        rx.script(
            """
            // Ocultar inmediatamente con CSS inline
            const hideStyle = document.createElement('style');
            hideStyle.textContent = `
                a.css-tww8i9, 
                a[href="https://reflex.dev"] {
                    display: none !important;
                    visibility: hidden !important;
                    opacity: 0 !important;
                }
            `;
            document.head.appendChild(hideStyle);
            
            // Eliminar permanentemente después
            function removeReflexElements() {
                const elements = document.querySelectorAll([
                    'a.css-tww8i9',
                    'a[href="https://reflex.dev"]'
                ].join(','));
                
                elements.forEach(el => el.remove());
            }
            
            // Ejecutar múltiples veces
            removeReflexElements();
            setInterval(removeReflexElements, 50);
            """
        ),
        add_customer_button(),
        rx.table.root(
            rx.table.header(
                #Encabezado de la tabla
                rx.table.row(
                    rx.table.column_header_cell("User"),
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Gender"),
                    rx.table.column_header_cell("Acciones"),
                ),
            ),

            #Cuerpo de la tabla
            rx.table.body(
                rx.foreach(State.users, sow_user),
            ),

            #rx.table.body(
            #    rx.table.row(
            #        rx.table.cell("Danilo Sousa"),
            #        rx.table.cell("danilo@example.com"),
            #        rx.table.cell("Male"),
            #    ),
            #    rx.table.row(
            #        rx.table.cell("Zahra Ambessa"),
            #        rx.table.cell("zahra@example.com"),
            #        rx.table.cell("Female"),
            #    ),
            #),
            on_mount=State.load_users,
            variant="surface",
            size="3",
            margin_top="20px"
        ),

        graph(),

        width="100%",
        align="center",
        justify="center",
        padding="40px 0px",

        # Añadir el CSS personalizado
        style=rx.style.Style({
            "import": "/hide-reflex.css"
        })

    )


app = rx.App(
    theme=rx.theme(
        radius="large", 
        accent_color="teal",
        appearance="dark",
    ),
)
app.add_page(
    index,
    title="App de Datos de Clientes",
    description="Una aplicación sencilla para gestionar datos de clientes.",
    on_load=State.transform_data,
)
