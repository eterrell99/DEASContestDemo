import { useRef } from 'react';
import { FaBars, FaTimes } from 'react-icons/fa';
import '../MainPage/mainpage.scss';
import { Link } from 'react-router-dom';
import Logo from '../MainPage/UALogo.png';

function Navbar() {
  const navRef = useRef();

  const showNavbar = () => {
    navRef.current.classList.toggle('responsive_nav');
  };

  return (
    <header>
      <img
        style={{
          borderRadius: '3px',
          width: '80px',
        }}
        src={Logo}
        alt=""
      />
      <nav ref={navRef}>
        <Link className="nav-link" to="/">
          Home
        </Link>
        <Link className="nav-link" to="/submit">
          Submit
        </Link>
        <Link className="nav-link" to="/about-us">
          About Us
        </Link>
        <button className="nav-btn nav-close-btn" onClick={showNavbar}>
          <FaTimes />
        </button>
      </nav>
      <button className="nav-btn" onClick={showNavbar}>
        <FaBars />
      </button>
    </header>
  );
}

export default Navbar;
