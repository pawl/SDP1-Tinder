/**
 * jTinder initialization
 */
 (function($) {
    "use strict"; // Start of use strict

    var setupZStack = function() {
        var items = $('#tinderslide .pane');
        var numItems = items.length;
        $.each(items, function(i, item) {
            $(item).data('stack-index', numItems - i);
            $(item).attr('data-stack-index', numItems - i);
            $(item).addClass('in-the-game');
            if (i == (numItems - 1) )
                $(item).addClass('top');
        });
    }

    var updateZStack = function() {
        $('#tinderslide .discarded').remove();
        var items = $('#tinderslide .pane.in-the-game');
        var numItems = items.length;
        items.removeClass('top');
        $.each(items, function(i, item) {
            // $(item).data('stack-index', numItems - i);
            $(item).attr('data-stack-index', numItems - i);
            $(item).attr("style", "");
            if (i == (numItems - 1) )
                $(item).addClass('top');
        });
        if (items.length == 1) {
            $('#control').addClass("hide");
            $('#thankyou').removeClass("hide");
            $('#thankyou .winner').html($(items[0]).data('name'));
            var uid = $(items[0]).data('image-id');
            if (typeof uid !== "undefined") {
                $.ajax({
                    url: context.voteUrl(uid),
                    type: "POST",
                    data: {},
                    success: function () {
                        console.log("Voted on image " + uid);
                    },
                    error: function (data) {
                        console.log("Error voting for image " + uid);
                        console.log(data);
                    }
                });
            }
        }
    }

    $(document).ready(function() {
        setupZStack();
        var onLikeOrDislike = function (isLike, item) {
            var uid = item.data('image-id');
            var url = isLike? context.swipeRightUrl(uid): context.swipeLeftUrl(uid);
            var swipeDirection = isLike? 'right': 'left';
            if (typeof uid !== "undefined") {
                $.ajax({
                    url: url,
                    type: "POST",
                    data: {},
                    success: function () {
                        console.log("Swiped " + swipeDirection + " on image " + uid);
                    },
                    error: function (data) {
                        console.log("Error swiping " + swipeDirection + " on image " + uid);
                        console.log(data);
                    }
                });
            }
        }

        $("#tinderslide").jTinder({
            // dislike callback
            onDislike: function (item) {
                // set the status text
                $('#status').html('Dislike image ' + (item.index()+1));
                onLikeOrDislike(false, item);
                $(item).removeClass('in-the-game').removeClass('top').addClass('discarded');
                $(item).removeAttr('data-stack-index');
                $(item).prependTo('#tinderslide ul');
                $(item).remove();
                updateZStack();
            },
            // like callback
            onLike: function (item) {
                // set the status text
                $('#status').html('Like image ' + (item.index()+1));
                onLikeOrDislike(true, item);
                var discardedElements = $('#tinderslide .pane.discarded');
                if(discardedElements.length > 0) {
                    $(item).insertAfter(discardedElements.last());
                } else {
                    console.log("Prepending!");
                    $(item).prependTo('#tinderslide ul');
                }
                updateZStack();
                // console.log(item);
                // console.log($(item));
                // $(item).attr("style", "");
            },
            animationRevertSpeed: 200,
            animationSpeed: 400,
            threshold: 1,
            likeSelector: '.like',
            dislikeSelector: '.dislike'
        });

        /**
         * Set button action to trigger jTinder like & dislike.
         */
        $('.actions .like').click(function(e){
            e.preventDefault();
            $("#tinderslide").jTinder('like');
            $('#tinderslide .in-the-game').removeAttr("style");
        });
        $('.actions .dislike').click(function(e){
            e.preventDefault();
            $("#tinderslide").jTinder('dislike');
            $('#tinderslide .in-the-game').removeAttr("style");
        });

        // $( "#tinderslide .in-the-game" ).change(function() {
        //     $('#tinderslide .in-the-game').removeAttr("style");
        // });
    });
})(jQuery); // End of use strict
