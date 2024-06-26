const fileInput = document.getElementById("fileSelect");
const imageInline = document.querySelector(".image-inline")
let files = []

function preview() {
    imageInline.innerHTML = ""

    for(let i = 0; i <= files.length; i++) {
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

function delImage(index) {
  files.splice(index, 1)
  preview()
}

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