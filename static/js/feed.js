"use strict";

const jwt = getJWTFromCookie();
const jwt_data = parseJwt(jwt);

let currentEditingTweet = {
    "id": "",
    "content": ""
};



async function deleteTweet(tweet_id) {
    console.log(tweet_id);
    // Connect to the api and delete it from the "database"
    const connection = await fetch(`/api/tweet/${tweet_id}`, {
        method: "DELETE",
        headers: {
            'Authorization': `Bearer ${jwt}`
        }
    });
    if (!connection.ok) {
        alert("uppps... try again");
        return;
    }

    document.getElementById(`tweet-${tweet_id}`).remove();
}

function htmlAddTweetToFeed(tweet, position = "beforeend") {
    let deleteIcon = "";
    let editIcon = "";
    if (jwt_data.username == tweet.username) {
        deleteIcon = `<button type='button' onclick="deleteTweet('${tweet.id}')"><i class="cursor-pointer fa-solid fa-trash-can"></i></button>`;
        editIcon = `<button type='button' onclick="toggleTweetModal('${tweet.id}')"><i class="fa-solid fa-pen-to-square"></i></button>`;
    }

    if (tweet.user_profile_picture_path == "" || tweet.user_profile_picture_path == null) {
        tweet.user_profile_picture_path = "placeholder.png"
    }

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
                <div class="flex gap-12 w-full mt-4 text-lg">
                    <button type='button' onclick="" class="ml-auto"><i class="cursor-pointer fa-solid fa-message"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-heart"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-retweet"></i></button>
                    <button type='button' onclick=""><i class="cursor-pointer fa-solid fa-share-nodes"></i></button>
                    ${deleteIcon}
                    ${editIcon}
                </div>
            </div>
        </div>
    </div>
    `;

    let tweetsDiv = document.getElementById("tweets");
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
    tweetsDiv.insertAdjacentHTML(position, htmlTweetTemplate);
}


function htmlDisplayTweets(tweets) {
    for (let i = 0; i < tweets.length; i++) {
        const tweet = tweets[i];
        htmlAddTweetToFeed(tweet, "beforeend");
    }
}

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

    for (let i = 0; i < tweets.length; i++) {
        const tweet = tweets[i]
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
        tweets[i].user_profile_picture_path = user.picture_path;
    }

    // Display tweets
    htmlDisplayTweets(tweets);
}

async function submitTweet() {
    let tweet_content = document.getElementById("txt-tweet").value;

    const tweet = {
        "content": tweet_content
    };

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
    const createdTweet = JSON.parse(await connection.text());
    htmlAddTweetToFeed(createdTweet, "afterbegin");

}

async function editTweet() {
    currentEditingTweet.content = document.getElementById("tweet-modal-text").value;

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
    const createdTweet = JSON.parse(await connection.text());

    document.getElementById(`tweet_content-${createdTweet.id}`).innerText = createdTweet.content
    document.getElementById("tweetModal").classList.add("hidden");

}


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
    document.getElementById("tweet-modal-text").value = tweet.content;

    // Store the currently editing tweet details so we can replace the content in HTML too.
    currentEditingTweet.content = tweet.content;
    currentEditingTweet.id = tweet.id;
}

getTweets();
