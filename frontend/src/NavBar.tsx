import type { Component } from 'solid-js';

type NavBarProps = {
    refreshFunc: () => Promise<void>
}

const NavBar: Component<NavBarProps> = (props: NavBarProps) => {
    return (
        <header class="navbar bg-secondary">
            <section class="navbar-section">
                <h1>dbt Jobs</h1>
            </section>

            <section class="navbar-section">
                <button class="btn" onClick={props.refreshFunc}>Refresh Data</button>
            </section>
        </header>
    )
};

export default NavBar;
