import { Controller } from "https://unpkg.com/@hotwired/stimulus/dist/stimulus.js"

export default class extends Controller {
    async playOnce(box) {
        alert("test")
        let url = box.params.url;
        await fetch(url)
    }
}