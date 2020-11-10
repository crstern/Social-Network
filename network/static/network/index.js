document.addEventListener("DOMContentLoaded", () => {
    const edditButtons = document.querySelectorAll(".edit-btn");
    edditButtons.forEach((element) => {
        element.addEventListener("click",() => {
            const editForm = document.querySelector(`#edit-form-${element.id}`)
            const postToEdit = document.querySelector(`#post-body-${element.id}`)
            editForm.style.display = "block";
            postToEdit.style.display = "none";
            element.style.display = "none";

            document.querySelector(`#cancel-${element.id}`).addEventListener("click", () => {
                console.log("clicked")
                editForm.style.display = "none";
                postToEdit.style.display = "block";
                element.style.display = "inline-block";
            })
        });
    });


    const likeButtons = document.querySelectorAll(".like-btn");
    likeButtons.forEach(element => {
        element.addEventListener("click", () => {
            const postId = element.id.substring(5);
            const likeCouneter = document.querySelector(`#like-counter-${postId}`)
            fetch(`/like/${postId}`, {
                method:"GET"
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
                likeCouneter.innerHTML = result.currentCounter
                element.innerHTML = result.buttonContent
            })
        })
    })

    const unlikeButtons = document.querySelectorAll(".unlike-btn");
    unlikeButtons.forEach(element => {
        element.addEventListener("click", () => {
            const postId = element.id.substring(7);
            const likeCouneter = document.querySelector(`#like-counter-${postId}`)
            
            fetch(`/like/${postId}`, {
                method:"GET"
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
                likeCouneter.innerHTML = result.currentCounter
                element.innerHTML = result.buttonContent
            })
        })
    })
})
