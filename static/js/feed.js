"use strict";

// Read the JWT (JSON web token) from cookies, and store them in a global variable, so everyone can use it
const jwt = getJWTFromCookie();
const jwt_data = parseJwt(jwt);

// Store the tweet we are currently editing in the modal window
let currentEditingTweet = {
    "id": "",
    "content": ""
};

async function deleteTweet(tweet_id) {
    console.log(tweet_id);
    // Connect to the api and delete it from the "database"
    const connection = await fetch(`/api/tweet/${tweet_id}`, {
        // HTTP Method, in this case delete
        method: "DELETE",
        // Pass the JWT token as authentication header (so we have access to stuff)
        headers: {
            'Authorization': `Bearer ${jwt}`
        }
    });
    if (!connection.ok) {
        // If there's any error in the response, display an error alert
        alert("uppps... try again");
        return;
    }

    // Delete the tweet from the UI in the DOM
    document.getElementById(`tweet-${tweet_id}`).remove();
}

// Add tweet to the UI
function htmlAddTweetToFeed(tweet, position = "beforeend") {
    let deleteIcon = "";
    let editIcon = "";
    // If the JWT data is the same as the tweet's username (user owns tweet), show the edit and delete icon
    if (jwt_data.username == tweet.username) {
        deleteIcon = `<button type='button' onclick="deleteTweet('${tweet.id}')"><i class="cursor-pointer fa-solid fa-trash-can"></i></button>`;
        editIcon = `<button type='button' onclick="toggleTweetModal('${tweet.id}')"><i class="fa-solid fa-pen-to-square"></i></button>`;
    }

    // If the user has no profule picture, then show the placeholder profile pic instead
    if (tweet.user_profile_picture_path == "" || tweet.user_profile_picture_path == null) {
        tweet.user_profile_picture_path = "placeholder.png"
    }

    // Template for a single tweet element on the UI
    let htmlTweetTemplate = `
    <div id="tweet-${tweet.id}" class="p-4 border-t border-slate-200">
        <div class="flex">
            <img class="flex-none w-12 h-12 rounded-full" src="/static/images/profiles/${tweet.user_profile_picture_path}" alt="profile_pic">
            <div class="w-full pl-4">
                <p class="font-bold">
                <a href='/profile/${tweet.username}'>@${tweet.username}</a> (Created at ${tweet.created})
                </p>
                <div class="pt-2" id="tweet_content-${tweet.id}">
                    ${tweet.content}
                </div>
                <div class="pt-2" id="tweet_picture-${tweet.id}">
                    <img src="/static/images/tweets/${tweet.picture_path}" alt="">
                </div>
                <div class="flex gap-12 w-full mt-4 text-lg">
                    <button type='button' onclick="" class="ml-auto"><i class="cursor-pointer fa-solid fa-message"></i></button>
                    ${deleteIcon}
                    ${editIcon}
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-heart"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-retweet"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-share-nodes"></i></button>
                </div>
            </div>
        </div>
    </div>
    `;

    let tweetsDiv = document.getElementById("tweets");
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
    // Inset tweet to the UI with specific order
    tweetsDiv.insertAdjacentHTML(position, htmlTweetTemplate);
}

// Take all tweets from input, and display each tweet one by one.
// This is just a wrapper function to make it nicer
function htmlDisplayTweets(tweets) {
    for (let i = 0; i < tweets.length; i++) {
        const tweet = tweets[i];
        htmlAddTweetToFeed(tweet, "beforeend");
    }
}

// Get tweets from API and database, adn display them too.
async function getTweets() {
    // Connect to the api and get all the tweets from the database
    const connection = await fetch(`/api/tweets`, {
        method: "GET",
        headers: {
            'Authorization': `Bearer ${jwt}`
        }
    });
    if (!connection.ok) {
        alert("uppps...try again");
        return;
    }
    // Parse the string into a json
    const tweets = JSON.parse(await connection.text());

    // Loop over all tweets and fetch user information for each of them
    for (let i = 0; i < tweets.length; i++) {
        const tweet = tweets[i]
        // get the user that owns the tweet
        const connection = await fetch(`/api/user/${tweet.username}`, {
            method: "GET",
            headers: {
                'Authorization': `Bearer ${jwt}`
            }
        });
        if (!connection.ok) {
            alert("uppps...try again");
            return;
        }
        // Parse the string into a json
        const user = JSON.parse(await connection.text());
        // Set the tweet's profile picture path to the user's profile picture path
        tweets[i].user_profile_picture_path = user.picture_path;
    }

    // Display all tweets
    htmlDisplayTweets(tweets);
}

// Create new tweet (both datbase and UI)
async function submitTweet() {
    let txt_tweet = document.getElementById("txt-tweet")
    let tweet_content = txt_tweet.value;

    // --------- Validate input via JS
    const data_min = parseInt(txt_tweet.getAttribute("data-min"))
    const data_max = parseInt(txt_tweet.getAttribute("data-max"))

    if (!validate_text_length(tweet_content, data_min, data_max)) {
        txt_tweet.classList.add("validate_error");
        txt_tweet.style.backgroundColor = validate_error_color;
        return;
    }

    txt_tweet.classList.remove("validate_error");
    txt_tweet.style.backgroundColor = "initial";
    // ---------------------------

    // We only get here if all validation passes

    const tweet = {
        "content": tweet_content
    };

    // Send request to API with autentication to create tweet
    const connection = await fetch(`/api/tweet`, {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${jwt}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tweet)
    });
    if (!connection.ok) {
        alert("uppps... try again");
        return;
    }
    // recieve the full created tweet from the database
    const createdTweet = JSON.parse(await connection.text());
    // Add tweet to the UI
    htmlAddTweetToFeed(createdTweet, "afterbegin");

}

async function editTweet() {
    // Get the new text for the tweet
    let txt_tweet = document.getElementById("tweet-modal-text")
    // Set the current tweet as the currently edited tweet
    currentEditingTweet.content = txt_tweet.value;

    let tweet_content = txt_tweet.value;

    // ----- Validate input via JS
    const data_min = parseInt(txt_tweet.getAttribute("data-min"))
    const data_max = parseInt(txt_tweet.getAttribute("data-max"))

    if (!validate_text_length(tweet_content, data_min, data_max)) {
        txt_tweet.classList.add("validate_error");
        txt_tweet.style.backgroundColor = validate_error_color;
        return;
    }

    txt_tweet.classList.remove("validate_error");
    txt_tweet.style.backgroundColor = "initial";
    // ---------------------------

    // Send patch request to edit the tweet with the new content
    const connection = await fetch(`/api/tweet`, {
        method: "PATCH",
        headers: {
            'Authorization': `Bearer ${jwt}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(currentEditingTweet)
    });
    if (!connection.ok) {
        alert("uppps... try again");
        return;
    }
    // Receive the new tweet back from the database
    const createdTweet = JSON.parse(await connection.text());

    // Update teh existing tweet's content on the UI
    document.getElementById(`tweet_content-${createdTweet.id}`).innerText = createdTweet.content
    // Hide editing modal window
    document.getElementById("tweetModal").classList.add("hidden");

}

// This funciton shows and hides the editing modal window
async function toggleTweetModal(tweet_id) {
    let tweetModal = document.getElementById("tweetModal");
    tweetModal.classList.toggle("hidden");
    tweetModal = document.getElementById("tweetModal");

    // Check if tweet ID undefined https://stackoverflow.com/questions/858181/how-to-check-a-not-defined-variable-in-javascript
    // This is when we close the modal window.
    if (tweet_id == null) {
        // Empty all values for later reuse (in case someone clicks a different edit button)
        document.getElementById("tweet-modal-text").value = "";
        currentEditingTweet.content = "";
        currentEditingTweet.id = "";
        return;
    }

    // Get the tweet from the database
    const connection = await fetch(`/api/tweet/${tweet_id}`, {
        method: "GET",
        headers: {
            'Authorization': `Bearer ${jwt}`
        }
    });
    if (!connection.ok) {
        alert("uppps...try again");
        return;
    }

    // Parse the string into a json
    const tweet = JSON.parse(await connection.text());
    // SHow the tweet's content in the input field
    document.getElementById("tweet-modal-text").value = tweet.content;

    // Store the currently editing tweet details globally so we can replace the content in HTML too.
    currentEditingTweet.content = tweet.content;
    currentEditingTweet.id = tweet.id;
}



// ---------------------------- Upload tweet picture ---------------------------
// Source https://attacomsian.com/blog/uploading-files-using-fetch-api
const input = document.getElementById('upload-tweet-picture');

// add event listener for picture selection (no submit button needed)
input.addEventListener('change', () => {
    // get the file from the input
    let file = input.files[0]
    // add file to FormData object (needed for upload)
    const fd = new FormData();
    fd.append('upload', file);

    // send `POST` request (with authentication)
    fetch(`/api/tweet/${currentEditingTweet.id}`, {
            method: 'POST',
            body: fd,
            headers: {
                'Authorization': `Bearer ${jwt}`,
            }
        })
        .then(res => res.json())
        .then(json => console.log(json))
        .catch(err => console.error(err));
});
// -----------------------------------------------------------------------------


// When the page loads, get all tweets
getTweets();
