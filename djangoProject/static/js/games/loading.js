$(document).ready(function () {
    let interval;
    let loadingBarInterval;

    $(".show-loading").click(function () {
        // Add a delay of 1 second before showing the loading screen
        interval = setTimeout(function () {
            console.log("Loading screen activated!");
            $(".container").hide();
            $("#loading").show();

            // Array of funny and engaging game-related loading messages
            var messages = [
                "Loading game data... making sure the dragons are fed 🐉.",
                "Hang tight! The goblins are organizing your inventory. 🧙‍♂️",
                "Updating stats... your level of awesomeness just increased! ✨",
                "Downloading loot... hope you're ready for some epic treasures! 💎",
                "Synchronizing with the wizard's server... patience is a virtue! 🔮",
                "The blacksmith is sharpening your swords... almost done! ⚔️",
                "Gathering allies and enemies... it's a busy tavern tonight! 🍻",
                "Recharging mana crystals... these things take time, you know! 🔋",
                "The dungeon boss is getting dressed... you’ll meet them soon! 👹",
                "Rebuilding pixel-perfect landscapes... it’s a lot of pixels! 🎨",
                "Calling the bard to sing a song while you wait... 🎵 ‘Loading time!’",
                "Unlocking secret achievements... we’ll tell you if you earn one! 🏆",
                "Checking game physics... do portals still break space-time? 🌀",
                "Polishing your character’s shoes... yes, that’s totally important. 👞",
                "Repainting the castle walls... it’s gotta look good for you! 🏰",
            ];

            // Show an initial random message
            var randomMessage = messages[Math.floor(Math.random() * messages.length)];
            $("#loading-message").text(randomMessage);

            // Fake loading bar
            let progress = 0;
            loadingBarInterval = setInterval(function () {
                progress += Math.random() * 10; // Increase progress randomly to simulate a quicker load
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(loadingBarInterval);
                }
                $("#loading-bar").css("width", progress + "%");
            }, 500);

            // Change the message every 5 seconds
            setInterval(function () {
                var randomMessage = messages[Math.floor(Math.random() * messages.length)];
                $("#loading-message").text(randomMessage);
            }, 5000);
        }, 1000);
    });

    // Reset loading screen when navigating back
    $(window).on('pageshow', function () {
        console.log("Page shown (navigated back)");
        clearInterval(interval);
        clearInterval(loadingBarInterval);
        $(".container").show();
        $("#loading").hide();
    });
});
