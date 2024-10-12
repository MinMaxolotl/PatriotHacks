import './ImageButton.css';


function ImageButton(props)
{
    return (
        <div className="ImageButton">
            <input type='file' onChange={props.onImageAdded} />
        </div>
    );
}
export default ImageButton;