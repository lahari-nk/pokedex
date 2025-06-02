# pokedex
⚡ Pokédex - Interactive Pokémon Database
A modern, interactive Pokédex web application built with Streamlit that allows users to search and explore Pokémon data through an intuitive interface.


🌟 Features


🔍 Dual Search Methods

Search by Name: Find Pokémon using partial name matching with intelligent substring search

Search by Type: Filter Pokémon by primary and secondary types using dropdown menus


📊 Comprehensive Pokémon Details

Complete base stats (HP, Attack, Defense, Sp. Atk, Sp. Def, Speed)

Visual stat bars with proportional scaling

Type badges with authentic Pokémon type colors

Generation and Legendary status information

Pokédex number and official names


🎨 Modern User Interface

Responsive grid layout for Pokémon browsing

Gradient backgrounds and smooth animations

Professional card-based design

Mobile-friendly responsive columns

Intuitive navigation with sidebar controls


📈 Dataset Insights

Real-time statistics display

Total Pokémon count, generations, types, and legendary count

Automatic data validation and error handling


🖥️ Usage Examples


Search by Name:

Select "Search by Name" from the sidebar

Type any part of a Pokémon's name (e.g., "pika" for Pikachu)

Click on any result to view detailed stats


Search by Type:

Select "Search by Type" from the sidebar

Choose a primary type from the first dropdown

Optionally select a secondary type for dual-type filtering

Browse results in the grid layout

Click any Pokémon to see complete information


🛠️ Technical Details


Built With:

Streamlit - Web application framework

Pandas - Data manipulation and analysis

Requests - HTTP library (for future enhancements)


Key Functions:

load_pokemon_data() - Loads and caches CSV data

find_similar_names() - Implements substring matching for name search

display_pokemon_stats() - Renders detailed Pokémon information

get_type_color() - Maps Pokémon types to authentic colors


📁 Project Structure


pokedex/

├── pokedex.py          # Main Streamlit application

├── pokemon.csv         # Pokémon dataset (not included)

├── README.md          # Project documentation

└── requirements.txt   # Python dependencies (optional)


🎯 Future Enhancements

Pokémon images integration

Advanced filtering options (generation, stats range)

Comparison tool between multiple Pokémon

Export functionality for filtered results

Dark/light theme toggle

Pokémon evolution chain display


🙏 Acknowledgments

Pokémon data structure inspired by the classic Pokédex format

Type colors based on official Pokémon franchise styling

Built with ❤️ for Pokémon trainers and data enthusiasts
