const fileInput = document.getElementById("id_image");
const imageInline = document.querySelector(".image-inline")
const btnSubmit = document.querySelector("button[type='submit']")
const pathname = window.location.pathname
let gallery = new Array()
let files = new Array()
let deletedFiels = new Array()

async function fetchGallery() {
  try {
    const response = await fetch(pathname, {
      method: "PATCH",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      }
    })
    if(!response.ok) {
      throw new Error("Network response was not ok")
    }
    const data = await response.json()
    const gallery = JSON.parse(data)
    return gallery
  } catch(error) {
    console.error("Error fetching gallery: ", error)
  }
}

async function fetchDelImage(image_id) {
  try {
    const response = await fetch(pathname + image_id, {
      method: "DELETE",
      headers: {
        "Accept": "application",
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      }
    })
  } catch(error) {
      console.error("Error fetching del image", error)
  }
}

function previewGallary() {
  for(let obj of gallery) {
    let figure = document.createElement("figure")
    let figCap = document.createElement("figcaption")
    let btnDel = document.createElement("span")
    let imagePath = obj.fields.image
    let imagePathDivided = imagePath.split("/")
    let name = imagePathDivided[imagePathDivided.length - 1]
    let img = document.createElement("img")

    figCap.innerText = name
    btnDel.innerText = "X"
    btnDel.className = "btn-del"
    
    btnDel.setAttribute("onClick", `delInGallery(${obj.pk})`)
    img.setAttribute("src", "/media/" + imagePath)
    figure.appendChild(figCap)
    figure.appendChild(btnDel)
    figure.insertBefore(img, figCap)
    imageInline.appendChild(figure)
  }
}

function preview() {
  imageInline.innerHTML = ""

  previewGallary()

  for(let i = 0; i < files.length; i++) {
    let reader = new FileReader()
    let figure = document.createElement("figure")
    let figCap = document.createElement("figcaption")
    let btnDel = document.createElement("span")
    
    figCap.innerText = files[i].name
    btnDel.innerText = "X"
    btnDel.className = "btn-del"
    
    btnDel.setAttribute("onClick", `delImage(${i})`)
    figure.appendChild(figCap)
    figure.appendChild(btnDel)
    
    reader.onload = ((file) => {
      return (e) => {
        let img = document.createElement("img")
        img.setAttribute("src", e.target.result)
        figure.insertBefore(img, figCap)
      }
    })(false)
    
    imageInline.appendChild(figure)
    reader.readAsDataURL(files[i])
  }
}

function delImage(id) {
  files.splice(id, 1)
  preview()
}

function delInGallery(id) {
  gallery = gallery.filter(obj => obj.pk != id)
  deletedFiels.push(id)
  preview()
}

document.addEventListener("DOMContentLoaded", async (event) => {
  if(location.href.match(/update/)) {
    gallery = await fetchGallery()
    preview()
  }
})

fileInput.addEventListener("change", (event) => {
  let newFiles = Array.from(event.target.files)

  newFiles = (newFiles.length <= 5) ? newFiles : newFiles.slice(0, 5);
  if(newFiles.length === 0) return;
  
  newFiles.forEach(file => {
    if(files.length === 0 || files.every(existingFile => existingFile.name != file.name)) {
      files.push(file)
    }
  })
  
  event.target.value = null
  preview()
})

btnSubmit.addEventListener("click", async (event) => {
  let formFile = document.querySelector('form[enctype="multipart/form-data"]')
  const dataTransfer = new DataTransfer()

  files.forEach(file => {
    let fileObg = new File([file], file.name, {
      type: "image/png, image/jpeg",
      lastModified: new Date(),
    })
    dataTransfer.items.add(fileObg)
  })
  
  deletedFiels.forEach(id => fetchDelImage(id))

  fileInput.files = dataTransfer.files
})