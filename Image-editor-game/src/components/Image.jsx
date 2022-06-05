import React, {useState} from 'react'
import Slider from '@mui/material/Slider';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';


function valuetext(value) {
    return `${value}`;
  }
export const Image = () => {
    let [img, setImage] = useState({
        original: ''
      })
    const handleFunc = async (e) => {
        e.preventDefault()
        let formData = new FormData(e.target)
        
        
        
        let data = {
            sha: formData.get('sharpen'),
            bri : formData.get('brightness'),
            cart : formData.get('cart'),
            tint : formData.get('tint'),
            blur: formData.get("blur"),
            sepia : formData.get("sepia"),
            duo_tone: formData.get("duo_tone"),
            splash : formData.get('splash'),
            img: formData.get('image')
 
        }

        console.log(data)

        const Upload =  await fetch('http://127.0.0.1:5000/game', {
            method: 'POST',
            body: formData
          })
    
          let resp = await Upload.json()

          setImage({
            original : resp['img'],
          })
          console.log(resp)
    }

  return (
      <>
    <div className='im'>
        <form  onSubmit={handleFunc}>
        
        <Box className="box" sx={{ width: 200 }}> 

        

            <Typography id="input-slider" gutterBottom>
            sharpen
                  </Typography>
            <Slider
            aria-label="Temperature"
            defaultValue={9.0}
            getAriaValueText={valuetext}
            valueLabelDisplay="auto"
            step={0.1}
            marks
            min={9.0}
            max={10.0}
            name='sharpen'
                  />

            <Typography id="input-slider" gutterBottom>
            brightness
                  </Typography>
            <Slider
            aria-label="Temperature"
            defaultValue={0.5}
            getAriaValueText={valuetext}
            valueLabelDisplay="auto"
            step={0.1}
            marks
            min={0.1}
            max={1.0}
            name='brightness'
                  />


            <div className="formss">
                <label htmlFor="cart">cartonize</label>
                <input type="checkbox" id="cart" name="cart" value="cart"  ></input>
            </div>

            <div className="formss">
                <label htmlFor="tint">tint</label>
                <input type="checkbox" id="tint" name="tint" value="tint"  ></input>
            </div>

            <div className="formss">
                <label htmlFor="blur">blur</label>
                <input type="checkbox" id="blur" name="blur" value="blur"  ></input>
            </div>

            <div className="formss">
                <label htmlFor="sepia">sepia</label>
                <input type="checkbox" id="sepia" name="sepia" value="sepia"  ></input>
            </div>

            <div className="formss">
                <label htmlFor="duo_tone">duo_tone</label>
                <input type="checkbox" id="duo_tone" name="duo_tone" value="duo_tone"  ></input>
            </div>

            <div className="formss">
                <label htmlFor="splash">splash</label>
                <input type="checkbox" id="splash" name="splash" value="splash"  ></input>
            </div>
      </Box>   

      <div className="input">
          <label htmlFor="image" className="label">Image :  </label>
                    <input type="file" id="image" name="image"
                        accept="image/*" className="file-custom"/>
      </div>

      <button type="submit">submit</button>
        </form>

        
    </div>

<div className="img-cont">
<img src={`data:image/png;base64,${img.original}`} alt="" />


</div>
</>
  )
}

export default Image