import { useState } from 'react'

import './App.css'



function App() {
 
  let [img, setImage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    const formData = new FormData(e.target);
    

    const Upload =  await fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        body: formData
      })

      let resp = await Upload.json()

      // console.log(resp)

      setImage({
        img : resp['success']
      })
      
    }
    
    console.log(img.img)
    
    

  return (
    
    <div className="App">
      <form  onSubmit={handleSubmit} className="Image-continer" encType="multipart/form-data">
          
          <div className="contents">
              
              <label htmlFor="image" className="label">Image :  </label>
              <input type="file" id="image" name="image" 
                  accept="image/*" className="file-custom"/>
              
          </div>


          <div className="btn">
              <button type="submit" className="submit-btn">Upload,,,</button>
          </div>
      </form>

    <div className="img-cont">
      <img  src={`data:image/png;base64,${img.img}`} id='image' />
    </div>
    
    </div>
  )
}

export default App
