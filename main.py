import streamlit as st
import streamlit_option_menu
from streamlit_extras.stoggle import stoggle
from processing import preprocess
from processing.display import Main
import random

# Setting the wide mode as default
st.set_page_config(layout="wide", page_title="Movie Recommender")

def load_custom_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {{
        font-family: 'Outfit', sans-serif !important;
        color: #f1f1f1 !important;
        background-color: #070707 !important;
    }}
    
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    
    @keyframes greenPulse {{
        0% {{ box-shadow: 0 0 5px rgba(0, 230, 118, 0.1); }}
        50% {{ box-shadow: 0 0 25px rgba(0, 230, 118, 0.6); }}
        100% {{ box-shadow: 0 0 5px rgba(0, 230, 118, 0.1); }}
    }}
    
    /* Sleek Sci-Fi Emerald for main interactive elements */
    .stButton>button {{
        background: linear-gradient(145deg, #111111 0%, #1a1a1a 100%) !important;
        color: #00E676 !important;
        border: 1px solid #00E676 !important;
        border-radius: 4px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        animation: greenPulse 3s infinite ease-in-out;
    }}
    
    .stButton>button:hover {{
        background: linear-gradient(145deg, #1a1a1a 0%, #222222 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 230, 118, 0.8) !important;
        animation: none; /* halt pulse on interactive hover */
    }}
    
    /* Sophisticated Headers */
    h1 {{
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: -webkit-linear-gradient(45deg, #00E676, #00B159);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 5px;
    }}
    
    h2, h3, p, span, div {{
        color: #f1f1f1 !important;
    }}
    
    /* Explicit Dropdown Color Fix */
    div[data-baseweb="select"] > div {{
        background-color: #111 !important;
        color: #f1f1f1 !important;
        border-color: #00E676 !important;
    }}
    
    /* Popover menu for select elements */
    ul[role="listbox"] {{
        background-color: #111 !important;
    }}
    
    li[role="option"] {{
        color: #f1f1f1 !important;
    }}
    
    /* Interactive Image scale on hover for Movie Posters */
    img {{
        border-radius: 12px;
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    }}
    img:hover {{
        transform: scale(1.08);
        box-shadow: 0 15px 30px rgba(0, 230, 118, 0.5);
        z-index: 10;
    }}
    
    /* Glassmorphism for internal text blocks */
    div[data-testid="stText"] {{
        opacity: 0.85;
    }}
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data():
    with Main() as bot:
        bot.main_()
        return bot.getter()


displayed = []

if "movie_number" not in st.session_state:
    st.session_state["movie_number"] = 0

if "selected_movie_name" not in st.session_state:
    st.session_state["selected_movie_name"] = ""

if "user_menu" not in st.session_state:
    st.session_state["user_menu"] = ""


def main():
    load_custom_css()

    def initial_options():
        # To display menu
        st.session_state.user_menu = streamlit_option_menu.option_menu(
            menu_title="The Cinematic Universe Awaits... 🌌",
            options=[
                "Discover Hidden Gems",
                "Explore Cinematic Lore",
                "Browse Full Catalog",
            ],
            icons=["film", "film", "film"],
            menu_icon="list",
            orientation="horizontal",
            styles={
                "container": {"background-color": "#111", "border": "1px solid #222", "border-radius": "10px", "padding": "5px"},
                "icon": {"color": "#00E676", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "--hover-color": "#1a1a1a",
                    "color": "#f1f1f1",
                    "font-family": "Outfit, sans-serif"
                },
                "nav-link-selected": {
                    "background-color": "#00E676",
                    "color": "#070707",
                    "font-weight": "800",
                    "box-shadow": "0 0 15px rgba(0, 230, 118, 0.4)"
                },
            }
        )

        if st.session_state.user_menu == "Discover Hidden Gems":
            recommend_display()

        elif st.session_state.user_menu == "Explore Cinematic Lore":
            display_movie_details()

        elif st.session_state.user_menu == "Browse Full Catalog":
            paging_movies()

    def recommend_display():

        st.markdown("<div style='text-align: center;'><h3 style='color: #888 !important; font-weight: 300 !important;'>Exclusive Collection</h3></div>", unsafe_allow_html=True)
        st.title("Premium Recommendations")

        selected_movie_name = st.selectbox("Search for a Masterpiece...", new_df["title"].values)

        rec_button = st.button("Recommend")
        if rec_button:
            st.session_state.selected_movie_name = selected_movie_name
            recommendation_tags(
                new_df, selected_movie_name, r"Files/similarity_tags_tags.pkl", "are"
            )
            recommendation_tags(
                new_df,
                selected_movie_name,
                r"Files/similarity_tags_genres.pkl",
                "on the basis of genres are",
            )
            recommendation_tags(
                new_df,
                selected_movie_name,
                r"Files/similarity_tags_tprduction_comp.pkl",
                "from the same production company are",
            )
            recommendation_tags(
                new_df,
                selected_movie_name,
                r"Files/similarity_tags_keywords.pkl",
                "on the basis of keywords are",
            )
            recommendation_tags(
                new_df,
                selected_movie_name,
                r"Files/similarity_tags_tcast.pkl",
                "on the basis of cast are",
            )

    def recommendation_tags(new_df, selected_movie_name, pickle_file_path, str):

        movies, posters = preprocess.recommend(
            new_df, selected_movie_name, pickle_file_path
        )
        st.subheader(f"Best Recommendations {str}...")

        rec_movies = []
        rec_posters = []
        cnt = 0
        # Adding only 5 uniques recommendations
        for i, j in enumerate(movies):
            if cnt == 5:
                break
            if j not in displayed:
                rec_movies.append(j)
                rec_posters.append(posters[i])
                displayed.append(j)
                cnt += 1

        # Columns to display informations of movies i.e. movie title and movie poster
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(rec_movies[0])
            st.image(rec_posters[0])
        with col2:
            st.text(rec_movies[1])
            st.image(rec_posters[1])
        with col3:
            st.text(rec_movies[2])
            st.image(rec_posters[2])
        with col4:
            st.text(rec_movies[3])
            st.image(rec_posters[3])
        with col5:
            st.text(rec_movies[4])
            st.image(rec_posters[4])

    def display_movie_details():

        selected_movie_name = st.session_state.selected_movie_name
        # movie_id = movies[movies['title'] == selected_movie_name]['movie_id']
        info = preprocess.get_details(selected_movie_name)

        with st.container():
            image_col, text_col = st.columns((1, 2))
            with image_col:
                st.text("\n")
                st.image(info[0])

            with text_col:
                st.text("\n")
                st.text("\n")
                st.title(selected_movie_name)
                st.text("\n")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Rating")
                    st.write(info[8])
                with col2:
                    st.text("No. of ratings")
                    st.write(info[9])
                with col3:
                    st.text("Runtime")
                    st.write(info[6])

                st.text("\n")
                st.write("Overview")
                st.write(info[3])
                st.text("\n")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Release Date")
                    st.text(info[4])
                with col2:
                    st.text("Budget")
                    st.text(info[1])
                with col3:
                    st.text("Revenue")
                    st.text(info[5])

                st.text("\n")
                col1, col2, col3 = st.columns(3)
                with col1:
                    str = ""
                    st.text("Genres")
                    for i in info[2]:
                        str = str + i + " . "
                    st.write(str)

                with col2:
                    str = ""
                    st.text("Available in")
                    for i in info[13]:
                        str = str + i + " . "
                    st.write(str)
                with col3:
                    st.text("Directed by")
                    st.text(info[12][0])
                st.text("\n")

        # Displaying information of casts.
        st.header("Cast")
        cnt = 0
        urls = []
        bio = []
        for i in info[14]:
            if cnt == 5:
                break
            url, biography = preprocess.fetch_person_details(i)
            urls.append(url)
            bio.append(biography)
            cnt += 1

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(urls[0])
            # Toggle button to show information of cast.
            stoggle(
                "Show More",
                bio[0],
            )
        with col2:
            st.image(urls[1])
            stoggle(
                "Show More",
                bio[1],
            )
        with col3:
            st.image(urls[2])
            stoggle(
                "Show More",
                bio[2],
            )
        with col4:
            st.image(urls[3])
            stoggle(
                "Show More",
                bio[3],
            )
        with col5:
            st.image(urls[4])
            stoggle(
                "Show More",
                bio[4],
            )

    def paging_movies():
        # To create pages functionality using session state.
        max_pages = movies.shape[0] / 10
        max_pages = int(max_pages) - 1

        col1, col2, col3 = st.columns([1, 9, 1])

        with col1:
            st.text("Previous page")
            prev_btn = st.button("Prev")
            if prev_btn:
                if st.session_state["movie_number"] >= 10:
                    st.session_state["movie_number"] -= 10

        with col2:
            new_page_number = st.slider(
                "Jump to page number",
                0,
                max_pages,
                st.session_state["movie_number"] // 10,
            )
            st.session_state["movie_number"] = new_page_number * 10

        with col3:
            st.text("Next page")
            next_btn = st.button("Next")
            if next_btn:
                if st.session_state["movie_number"] + 10 < len(movies):
                    st.session_state["movie_number"] += 10

        display_all_movies(st.session_state["movie_number"])

    def display_all_movies(start):

        i = start
        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]["movie_id"]
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies["title"][i])
                i = i + 1

        st.session_state["page_number"] = i
        
    def display_footer(new_df):
        st.markdown("<hr style='border: 1px solid rgba(0, 230, 118, 0.3); margin-top: 50px; margin-bottom: 30px; box-shadow: 0 0 10px rgba(0,230,118,0.2);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #00E676 !important;'>The Director's Cut</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns((2, 1))
        with col1:
            quotes = [
                '"May the Force be with you." - Star Wars, 1977',
                '"There\'s no place like home." - The Wizard of Oz, 1939',
                '"I\'m the king of the world!" - Titanic, 1997',
                '"Carpe diem. Seize the day, boys." - Dead Poets Society, 1989',
                '"I\'ll be back." - The Terminator, 1984',
                '"You talking to me?" - Taxi Driver, 1976',
                '"To infinity and beyond!" - Toy Story, 1995',
                '"Houston, we have a problem." - Apollo 13, 1995'
            ]
            selected_quote = random.choice(quotes)
            st.markdown(f"""
            <div style='background: #111; padding: 20px; border-radius: 10px; border-left: 4px solid #00E676; margin-top: 10px;'>
                <p style='font-size: 18px; font-style: italic; color: #f1f1f1; margin: 0;'>{selected_quote}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            if st.button("🎲 Surprise Me With a Masterpiece"):
                st.session_state.random_movie_trigger = random.choice(new_df["title"].values)

        if "random_movie_trigger" in st.session_state:
            st.markdown("<br><br>", unsafe_allow_html=True)
            # Hijack details display variable manually so it safely resolves in UI
            st.session_state.selected_movie_name = st.session_state.random_movie_trigger
            display_movie_details()

    new_df, movies, movies2 = load_data()
    initial_options()
    display_footer(new_df)


if __name__ == "__main__":
    main()
