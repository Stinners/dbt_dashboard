import type { Component } from 'solid-js';

const NavBar: Component = () => {
    return (
        <header class="navbar bg-secondary">
            <section class="navbar-section">
                <h1>dbt Jobs</h1>
            </section>

            <section class="navbar-section">
                <button class="btn">Refresh Data</button>
            </section>
        </header>
    )
};

export default NavBar;
