import './Header.css';
import logo from './Images/SpotiPic.svg'
function Header(props)
{
    return (
        <div className="Header">
            <img src={logo} id="logo" />
            <p>{props.textp}</p>
        </div>
    );
}

export default Header;