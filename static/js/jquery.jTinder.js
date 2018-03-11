/*
 * jTinder v.1.0.0
 * https://github.com/do-web/jTinder
 * Requires jQuery 1.7+, jQuery transform2d
 *
 * Copyright (c) 2014, Dominik Weber
 * Licensed under GPL Version 2.
 * https://github.com/do-web/jTinder/blob/master/LICENSE
 *
 * fork:
 * jTinder v.2.0.0
 * https://github.com/JoeSchr/jTinder-infinite
 * Requires jQuery 1.7+, jQuery transform2d
 *
 * Copyright (c) 2015, Joe Schroecker
 * Licensed under GPL Version 2.
 * https://github.com/JoeSchr/jTinder-infinite/blob/master/LICENSE
 */

;(function ($, window, document, undefined) {
    var pluginName = "jTinder",
        defaults = {
            onDislike: null,
            onLike: null,
            onImageLoading: null,
            beforeNextLoaded: null,
            onNextLoaded: null,
            animationRevertSpeed: 200,
            animationSpeed: 400,
            threshold: 1,
            loadNextThreshold: 5,
            likeSelector: '.like',
            dislikeSelector: '.dislike',
            nextSelector: null,
            itemSelector: '.infinite-item'
        };

    function Plugin(element, options) {
        this.element = element;
        this.settings = $.extend({}, defaults, options);
        this._defaults = defaults;
        this._name = pluginName;
        this.init(element);
    }

    Plugin.prototype = {

        init: function (element) {
            this.container = $(element).find("ul");
            this.noMoreData = false;
            this.panes = $(this.container.find(this.settings.itemSelector));
            this.index = this.panes.length-1; // faster if we just manage it ourselves and not recalculate evey next()
            this.nextUrl = this.fetchNextUrl($); // fetchNextUrl from current document
            this.currentPane = $(this.panes.last());
            this.paneWidth = this.currentPane.width();
            this.touchStart = false;
            this.xStart = 0;
            this.yStart = 0;
            this.scrollStart = 0;
            this.lastPosX = 0;
            this.lastPosY = 0;
            this.posX = 0;
            this.posY = 0;

            var isTouchSupported = "ontouchend" in document;
            this.downEvent = isTouchSupported ? "touchstart" : "mousedown";
            this.upEvent = isTouchSupported ? "touchend" : "mouseup";
            this.moveEvent = isTouchSupported ? "touchmove" : "mousemove";

            this.switchLazyImage(this.currentPane.find("img").first(), true);
            this.currentPane.show();
            this.prepareNext();



            $(element).bind(this.downEvent +" "+ this.moveEvent, $.proxy(this.handler, this));
            $(element).bind(this.upEvent, $.proxy(this.touchEndHandler, this));
        },

        next: function () {

            this.hideTopPane() // visually
            .done(function(){
                this.currentPane.remove();
                this.moveToNext()
            }.bind(this));// done
        },
        // returns promise for animate effects
        hideTopPane: function () {

            likePane.animate({'opacity': 0}, 1000);
            dislikePane.animate({'opacity': 0}, 1000);
            return this.currentPane.animate({'opacity': 0}, 500).promise()
        },

        moveToNext: function ()
        {
            if(this.index <=  this.settings.loadNextThreshold)
            {
                this.loadAjaxData();
                return
            }

            this.index--;
            this.currentPane = this.panes.eq(this.index);
            this.prepareNext();
        },

        prepareNext: function(pane)
        {
            pane = (pane)?(pane):(this.currentPane);
            var $next = pane.prev();
            this.switchLazyImage($next.find("img").first(), true);
            $next.show();
        },

        switchLazyImage: function($img, forceVisible)
        {
            $img = $img ? $img : this.currentPane.find("img").first();
            if(!forceVisible && !$img.is("[lazySrc]")) // not lazy yet
            {
               switchAttribute($img, "src", "lazySrc");
            }
            else // switch back
            {
                if($img.is("[lazySrc]")) // make visible if there a lazy
                    switchAttribute($img, "lazySrc", "src");
                if(this.settings.onImageLoading) // callback
                    this.settings.onImageLoading($img, this);
            }

        },

        loadAjaxData: function()
        {
            if(this.noMoreData)
            {
                if(this.settings.onNoMoreData)
                    this.settings.onNoMoreData();
                return;
            }

            if(!this.nextUrl) {  // first time or last time
                this.noMoreData = true; }

            if(this.settings.beforeNextLoaded) {
                this.settings.beforeNextLoaded(this)}


            $.ajax({url: this.nextUrl, context: this, async: true}).done(function(data,textStatus,jqXHR)
            {
                var $items = $(data).find(this.settings.itemSelector);

                this.container.prepend($items);
                this.panes = this.container.find(this.settings.itemSelector);
                var self = this;
                /*this.panes.find("img").each(function(){
                     var $this = $(this);
                     self.switchLazyImage($this);
                })*/

                this.index = this.panes.length-1;// combine old and new items
                this.currentPane = $(this.panes.eq(this.index));
                this.switchLazyImage(this.currentPane.find("img").first(), true); // switch back the active one
                this.prepareNext(); // an preload next
                this.currentPane.show();

                var oldUrl = this.nextUrl;
                this.nextUrl = this.fetchNextUrl($(data));
                if(!this.nextUrl || this.nextUrl == oldUrl)
                    noMoreData = true;

                if(this.settings.onNextLoaded) // callback
                    this.settings.onNextLoaded($items, this);

            });
        },



        fetchNextUrl: function($context) {
            var link;
            link = $context.find(this.settings.nextSelector);
            return (link.length > 0)? (link[0].href):(null);
        },

        dislike: function() {
            if(this.settings.onDislike) {
                this.settings.onDislike(this.currentPane);
            }
            this.next();
        },

        like: function() {
            if(this.settings.onLike) {
                this.settings.onLike(this.currentPane);
            }
            this.next();
        },

        calcPos: function (pageX, pageY) {
            var delta = {
                x: parseInt(pageX) - parseInt(this.xStart),
                y: parseInt(pageY) - parseInt(this.yStart)
            };
            this.posX = delta.x + this.lastPosX;
            this.posY = delta.y + this.lastPosY;
            return delta;
        },

        calcOpacity: function (delta) {
            var x = delta.x;
            var t = 1 + Math.abs(x);
            if (t > 100.0)
                t = 100.0;
            var y = Math.abs(delta.y);
            var s = 2.0 * Math.abs($(window).scrollTop() - this.scrollStart);
            if (s > y)
                y = s;
            var ratio = y / t;
            if(ratio > 1.0)
                x /= ratio;
            var opa = (Math.abs(x) / this.settings.threshold) / 100;
            if(opa > 1.0) {
                opa = 1.0;
            }
            return opa;
        },

        handler: function (ev) {
            if(! (ev.originalEvent.target == this.currentPane.find("img").first().get(0)) )
                return;

            switch (ev.type) {
                case this.downEvent:
                    if(this.touchStart === false) {
                        if(ev.type == 'mousedown')
                            ev.preventDefault();

                        this.touchStart = true;
                        this.xStart = ev.pageX || ev.originalEvent.touches[0].pageX;
                        this.yStart = ev.pageY || ev.originalEvent.touches[0].pageY;
                        this.scrollStart = $(window).scrollTop();
                    }
                case this.moveEvent:
                    if(this.touchStart === true) {
                        if(ev.type == 'mousemove')
                            ev.preventDefault();
                        var pageX = ev.pageX || ev.originalEvent.touches[0].pageX;
                        var pageY = ev.pageY || ev.originalEvent.touches[0].pageY;
                        var delta = this.calcPos(pageX, pageY);

                        var percent = delta.x * 100 / this.paneWidth;

                        var opa = this.calcOpacity(delta);
                        /*if (opa <= 0.1) // dont react to every little s#
                            return;*/

                        likePane = this.currentPane.find(this.settings.likeSelector);
                        dislikePane = this.currentPane.find(this.settings.dislikeSelector);

                        this.currentPane.css('opacity', 1-opa); // makes currentPane also opaque depending on delta

                        if (this.posX >= 0) {
                            this.currentPane.css('transform', "translate(" + this.posX + "px, 0px)");
                            likePane.css('opacity', opa);
                            dislikePane.css('opacity', 0);
                        } else if (this.posX < 0) {
                            this.currentPane.css('transform', "translate(" + this.posX + "px, 0px)");
                            dislikePane.css('opacity', opa);
                            likePane.css('opacity', 0);
                        }
                    }
                    break;
            }
        },

        touchEndHandler: function (ev) {
            if(ev.type == 'mouseup')
                ev.preventDefault();
            //else if(ev.type != "touchend")
            //    return // only handle this

            // if we didn't click on image return
            var img = this.currentPane.find("img").first().get(0);
            var target = ev.target || ev.originalEvent.target;
            if(!(target == img ) )
                return;

            //this.touchStart = false;
            if(this.touchStart)
                this.touchStart = false;
            else
                return // prevent doubleClick()

            // check leeway
            if (this.posX > 0) {
                this.like();
            } else if (this.posX <= 0) {
                this.dislike();
            }
        }
    };

    function switchAttribute($elem, attr, repl)
    {
        $elem.attr(repl, $elem.attr(attr));
        $elem.removeAttr(attr);
    };

    $.fn[ pluginName ] = function (options) {
        this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName, new Plugin(this, options));
            }
            else if ($.isFunction(Plugin.prototype[options])) {
                $.data(this, 'plugin_' + pluginName)[options]();
            }
        });

        return this;
    };

})(jQuery, window, document);
