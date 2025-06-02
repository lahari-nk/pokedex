import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Pokédex", page_icon='images/pokeball.png', layout="wide", initial_sidebar_state="expanded")

def load_css(file_name):
    with open(file_name) as styles:
        st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)

@st.cache_data
def load_pokemon_data():
    df = pd.read_csv('pokemon_data.csv')
    df.columns = df.columns.str.strip()
    return df    

def get_type_color(pokemon_type):
    type_colors = {
        'Normal': '#A8A878',   'Fire': '#F08030',     'Water': '#6890F0',
        'Electric': '#F8D030', 'Grass': '#78C850',    'Ice': '#98D8D8',
        'Fighting': '#C03028', 'Poison': '#A040A0',   'Ground': '#E0C068',
        'Flying': '#A890F0',   'Psychic': '#F85888',  'Bug': '#A8B820',
        'Rock': '#B8A038',     'Ghost': '#705898',    'Dragon': '#7038F8',
        'Dark': '#705848',     'Steel': '#B8B8D0',    'Fairy': '#EE99AC'
    }
    return type_colors.get(pokemon_type, '#68A090')

def display_pokemon_stats(pokemon_row):
    st.markdown(f"""
    <div class="pokemon-card">
        <h2>#{int(pokemon_row['#'])} - {pokemon_row['Name']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("Types:")
    with col2:
        type1_color = get_type_color(pokemon_row['Type 1'])
        st.markdown(f'<span class="type-badge" style="background-color: {type1_color}; color: white;">{pokemon_row["Type 1"]}</span>', 
                   unsafe_allow_html=True)
        if pd.notna(pokemon_row['Type 2']) and pokemon_row['Type 2'] != '':
            type2_color = get_type_color(pokemon_row['Type 2'])
            st.markdown(f'<span class="type-badge" style="background-color: {type2_color}; color: white;">{pokemon_row["Type 2"]}</span>', 
                       unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📊 Base Stats")
    
    stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    max_stat = 255
    for stat in stats:
        if stat in pokemon_row:
            stat_value = int(pokemon_row[stat])
            percentage = (stat_value / max_stat) * 100
            col1, col2, col3 = st.columns([2, 1, 3])
            with col1:
                st.write(f"**{stat}:**")
            with col2:
                st.write(f"{stat_value}")
            with col3:
                st.markdown(f"""
                <div class="stat-bar">
                    <div class="stat-fill" style="width: {percentage}%"></div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Generation:** {int(pokemon_row['Generation'])}")
    with col2:
        legendary_status = "Yes" if pokemon_row['Legendary'] else "No"
        if pokemon_row['Legendary']:
            st.success(f"**Legendary:** {legendary_status} ⭐")
        else:
            st.info(f"**Legendary:** {legendary_status}")

def find_similar_names(search_term, all_names, max_results=10):
    search_lower = search_term.lower()
    matches = []

    for name in all_names:
        if search_lower in name.lower():
            matches.append(name)
            if len(matches) >= max_results:
                break
    
    return matches

def main():
    load_css('styles/styles.css')
    df = load_pokemon_data()

    st.title("⚡ Pokédex")
    st.markdown("*Gotta catch 'em all!*")
    
    if df is not None:
        st.sidebar.title("🔍 Search Options")
        search_option = st.sidebar.radio(
            "Choose search method:",
            ["Search by Name", "Search by Type"]
        )

        if search_option == "Search by Name":
            st.header("🔤 Search Pokémon by Name")
            
            search_name = st.text_input("Enter Pokémon name:", placeholder="e.g., Pikachu, Charizard...")
            
            if search_name:
                all_names = df['Name'].tolist()
                similar_names = find_similar_names(search_name, all_names, 10)
                
                if similar_names:
                    st.subheader(f"Found {len(similar_names)} matching Pokémon:")
                    
                    cols = st.columns(min(3, len(similar_names)))
                    
                    for i, name in enumerate(similar_names):
                        with cols[i % 3]:
                            pokemon_data = df[df['Name'] == name].iloc[0]
                            if st.button(
                                f"#{int(pokemon_data['#'])} {name}", 
                                key=f"name_{i}",
                                use_container_width=True
                            ):
                                st.session_state.selected_pokemon = pokemon_data
                    
                    if 'selected_pokemon' in st.session_state:
                        st.markdown("---")
                        display_pokemon_stats(st.session_state.selected_pokemon)
                else:
                    st.warning("No Pokémon found with that name. Try a different spelling!")
        
        elif search_option == "Search by Type":
            st.header("🏷️ Search Pokémon by Type")
            
            type1_options = ['All'] + sorted([t for t in df['Type 1'].unique() if pd.notna(t)])
            type2_options = ['All'] + sorted([t for t in df['Type 2'].unique() if pd.notna(t) and t != ''])
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_type1 = st.selectbox("Select Type 1:", type1_options)
            
            with col2:
                selected_type2 = st.selectbox("Select Type 2 (optional):", type2_options)
            
            filtered_df = df.copy()
            
            if selected_type1 != 'All':
                filtered_df = filtered_df[filtered_df['Type 1'] == selected_type1]
            
            if selected_type2 != 'All':
                filtered_df = filtered_df[filtered_df['Type 2'] == selected_type2]
            
            if len(filtered_df) > 0:
                st.subheader(f"Found {len(filtered_df)} Pokémon:")
                
                num_cols = 4
                rows = len(filtered_df) // num_cols + (1 if len(filtered_df) % num_cols > 0 else 0)
                
                for row in range(rows):
                    cols = st.columns(num_cols)
                    for col_idx in range(num_cols):
                        pokemon_idx = row * num_cols + col_idx
                        if pokemon_idx < len(filtered_df):
                            pokemon = filtered_df.iloc[pokemon_idx]
                            with cols[col_idx]:
                                if st.button(
                                    f"#{int(pokemon['#'])} {pokemon['Name']}", 
                                    key=f"type_{pokemon_idx}",
                                    use_container_width=True
                                ):
                                    st.session_state.selected_pokemon_type = pokemon
                
                if 'selected_pokemon_type' in st.session_state:
                    st.markdown("---")
                    display_pokemon_stats(st.session_state.selected_pokemon_type)
            else:
                st.warning("No Pokémon found with the selected type combination.")
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("📈 Dataset Info")
        st.sidebar.info(f"Total Pokémon: {len(df)}")
        st.sidebar.info(f"Generations: {df['Generation'].nunique()}")
        st.sidebar.info(f"Legendary: {df['Legendary'].sum()}")
        st.sidebar.info(f"Types: {df['Type 1'].nunique()}")

if __name__ == "__main__":
    main()
