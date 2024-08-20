import streamlit as st

# Add custom CSS for full-page image layout and new sections
st.markdown("""
    <style>
/* Ensure the full-page container takes the entire viewport */
.full-page {
    height: 110vh;
    width: 100vw;
    margin: 0;
    padding: 0;
    margin-left: -37rem;
}

/* Top half with a full-width background image */
.top-half {
    width: 100%;
    height: 80%;
    background-image: url('https://media.istockphoto.com/id/1345991634/photo/artificial-intelligence-3d-robot-hand-finger-pointing-in-futuristic-cyber-space-metaverse.jpg?s=2048x2048&w=is&k=20&c=V86yEWYmg0sKIJLCjST4_LJ6d0O9kT5mKqNvTHcqbHM=');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    margin-top: -2rem;
}

/* Bottom half centered */
.bottom-half {
    width: 100%;
    height: auto;
    background-color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 2rem 0;
}

/* Card styles */
.card-container {
    display: flex;
    justify-content: space-around;
    width: 100%;
    margin-top: 2rem;
}

.card {
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 22%;
    height: 300px;  /* Increased card height */
    text-align: center;
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(49, 51, 63);
}

.card h2 {
    margin-bottom: 1rem;
    font-size: 24px;
}

.card p {
    font-size: 16px;
    line-height: 1.5;
}

/* Flex layout for section icons and text */
.section-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    width: 100%;
    padding: 2rem;
    margin-top: -40rem;
}

.section {
    width: 30%;
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.section img {
    width: 50px; /* Adjust icon size */
    height: 50px; /* Adjust icon size */
    margin-right: 1rem; /* Space between icon and text */
}

.section h2, .section p {
    margin: 0;
}

/* Image section styles */
.image-container {
    display: flex;
    justify-content: space-around;
    width: 100%;
    margin-top: 2rem;
}

.image-container img {
    width: 30%;
    height: 400px;  /* Set a fixed height for the images */
    object-fit: cover;  /* Maintain aspect ratio and cover the area */
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* Image between sections */
.image-between-sections {
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 2rem 0;
}

.image-between-sections img {
    max-width: 80%; /* Adjust width as needed */
    height: auto;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.left-sections, .right-sections {
    display: flex;
    flex-direction: column;
    width: 38%;
    margin-right: -23rem;
    margin-left: 8rem;
    margin-top: -7rem;
}
</style>

""", unsafe_allow_html=True)

# HTML and CSS layout
st.markdown("""
    <div class="full-page">
    <div class="top-half"></div>
    <div class="bottom-half">
        <!-- Content for the bottom half of the page -->
        <h1>Our Services</h1>
        <div class="card-container">
            <div class="card">
                <h2>Internal Store Transfers</h2>
                <p>Optimize internal transfers to ensure timely and efficient movement of stock between stores, improving availability and reducing overstock.</p>
            </div>
            <div class="card">
                <h2>Assortment Planning</h2>
                <p>Develop and execute strategic assortment plans to meet consumer demand, enhance product mix, and maximize sales opportunities.</p>
            </div>
            <div class="card">
                <h2>Replenishment Management</h2>
                <p>Automate replenishment processes to maintain optimal inventory levels, reduce stockouts, and ensure product availability across all locations.</p>
            </div>
            <div class="card">
                <h2>Inventory Optimization</h2>
                <p>Implement advanced inventory management techniques to balance stock levels, minimize holding costs, and increase overall efficiency.</p>
            </div>
        </div>
        <!-- Image section -->
        <div class="image-container">
            <img src="https://emc2rrspvpp.exactdn.com/wp-content/uploads/2022/02/Resource-1.jpg?lossy=1&quality=92&webp=92&ssl=1" alt="Image 1">
            <img src="https://emc2rrspvpp.exactdn.com/wp-content/uploads/2022/03/Resource-2.jpg?lossy=1&quality=92&webp=92&ssl=1" alt="Image 2">
            <img src="https://emc2rrspvpp.exactdn.com/wp-content/uploads/2024/01/2023-CMI-in-review.jpg?lossy=1&quality=92&webp=92&ssl=1" alt="Image 3">
        </div>
        <!-- Image between sections -->
        <div class="image-between-sections">
            <img src="https://zrtechsolutions.com/demo/html/technoit/assets/images/features.jpg" alt="Image Between Sections">
        </div>
        <!-- Sections with icons and text -->
        <div class="section-container">
            <div class="left-sections">
                <div class="section">
                    <img src="https://via.placeholder.com/50" alt="Pricing Icon">
                    <div>
                        <h2>Pricing</h2>
                        <p>Ronsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    </div>
                </div>
                <div class="section">
                    <img src="https://via.placeholder.com/50" alt="Delivery Icon">
                    <div>
                        <h2>Delivery</h2>
                        <p>Ronsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    </div>
                </div>
                <div class="section">
                    <img src="https://via.placeholder.com/50" alt="Support Icon">
                    <div>
                        <h2>Support</h2>
                        <p>Ronsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    </div>
                </div>
            </div>
            <div class="right-sections">
                <div class="section">
                    <img src="https://via.placeholder.com/50" alt="Experience Icon">
                    <div>
                        <h2>Experience</h2>
                        <p>Ronsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    </div>
                </div>
                <div class="section">
                    <img src="https://via.placeholder.com/50" alt="Products Icon">
                    <div>
                        <h2>Products</h2>
                        <p>Ronsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    </div>
                </div>
                <div class="section">
                    <img src="https://via.placeholder.com/50" alt="Approach Icon">
                    <div>
                        <h2>Approach</h2>
                        <p>Ronsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
