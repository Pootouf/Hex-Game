import { Controller } from "https://unpkg.com/@hotwired/stimulus/dist/stimulus.js"

export default class extends Controller {
    async playOnce(box) {
        console.log(box.params)
        let url = box.params.url;
        let response = await fetch(url)
        document.getElementsByTagName("html")[0].innerHTML = await response.text()
    }
}