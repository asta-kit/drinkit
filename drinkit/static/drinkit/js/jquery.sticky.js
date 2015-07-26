(function($){

	var Sticky = function(element, options) {

		var defaults = {

			/**
			 * In case of non-table elements,
			 * a sticky element can be bound to another element
			 * This other element could be the content that follows a header element
			 * When the content element(bindWith) scrolls out of screen, 
			 * disable sticky
			 * @type {String}
			 */
			bindWith: 'body'

		};


		//Standard jQuery plugin stuff
		this.options = $.extend(defaults, options);
		this.$el = $(element);


		//Properties needed across the plugin
		
		/**
		 * In case this is a table, the actual element will be the first row
		 * (not the table itself)
		 */
		this.$stickyEl = this.$el;


		/**
		 * The sticky element's width needs to be reaffirmed in case of a fixed position
		 * @type {Number}
		 */
		this.elWidth = this.$el.outerWidth();


		/**
		 * The sticky element's height
		 * Will be required to be subtracted from the top to monitor scroll top
		 * @type {Number}
		 */
		this.elHeight = 0;        //required in case sticky is applied on a non table along with a bindWidth element to check for scroll
		

		/**
		 * Required in order to set the correct left distance
		 * when sticky has a fixed position
		 * @type {Object}
		 */
		this.pos = this.$el.offset();


		//kickstart
		this.init();

	};



	/**
	 * Bootstrap the plugin based on the element (tag name)
	 */
	Sticky.prototype.init = function() {

		/**
		 * Sticky properties will change based on the type of element.
		 * In case of a table, the row with the table header elements will be sticky.
		 * In case of a non-table, the whole element will be sticky.
		 * --------------------------------------------------------------------------
		 * Check if this element is a table or not & init the sticky functionality accordingly
		 * 
		 * @type {Boolean}
		 */
		if(this.$el.prop('tagName').toLowerCase() !== 'table') {

			//this is not a table
			this.initStickyOnElement();

		} else {

			//this is a table
			this.initStickyOnTable();

		}

		//Initialize the window.scroll event handler
		this.scrollHandler();

	};



	/**
	 * Inititalize sticky on table element in a particular way
	 */
	Sticky.prototype.initStickyOnTable = function() {

		var 
			//First and last rows of the table
			$trFirst = $(this.$el.find('tr:first')),
			$trLast = $(this.$el.find('tr:last')),

			//TD elements of the last row in an array
			trLastTdArr = $trLast.find('td'),

			//Border spacing
			borderSpacingStr,
			xBorderSpacing,
			yBorderSpacing,


			//Top Margin (for fixed positioned sticky element)
			marginTop = 0
		;


		/**
		 * We ll use the table's height to toggle the sticky behavior on scroll
		 * We ll subtract the first row's height to get the appropriate elHeight
		 */
		this.elHeight = this.$el.height() - $trFirst.height();

		/**
		 * On applying a fixed position, the TH widths will get messed up
		 * Apply existing width explicitly and use them on the last row's TD elements as well.
		 * @param  {Number} idx [The index of the element in the loop]
		 * @param  {DOM} el [The TH element itself]
		 */
		$trFirst.find('th').each(function(idx, el) {

			//Fix the width of this TH element from the first row
			$(el).css('width', $(this).width());

			//Use the trLastTdArr to get the TD element from the last row
			$(trLastTdArr[idx]).css('width', $(this).width());

		});



		/**
		 * On tables with border-collapse set to the default (which is 'separate'), 
		 * a small spacing is seen on the top and left of the element when its sticky.
		 * To tackle this, get the X & Y value of that spacing and subtract it from the sticky TR.
		 */
		if(this.$el.css('border-collapse') === 'separate') {

			//Get the border spacing
			borderSpacingStr = this.$el.css('border-spacing');	//e.g: 2px 2px 


			//derive the X and Y values from borderSpacingStr
			xBorderSpacing = borderSpacingStr.split(' ')[0];	//e.g: 2px
			yBorderSpacing = borderSpacingStr.split(' ')[1];	//e.g: 2px
			

			//get rid of the 'px'
			marginTop = parseInt(yBorderSpacing.substring(0, yBorderSpacing.indexOf('px')), 10);

		}

		//Setup properties on the first row (sticky element) so that 
		//they kick in when it has position:fixed
		$trFirst
			.css('width', $trFirst.width())
			.css('top', 0 - marginTop)
			.css('left', this.pos.left)
		;

		/**
		 * Finally, since this is a table, we 'll set the first row to 
		 * be the sticky element
		 */
		this.$stickyEl = $trFirst;

	};



	/**
	 * Inititalize sticky on non-table element in a particular way
	 */
	Sticky.prototype.initStickyOnElement = function() {

		var 
			//Get the margin top of the element
			marginTopStr = this.$el.css('margin-top'), //e.g.: 10px 

			//Get rid of the 'px'
			marginTop = 0 - parseInt(marginTopStr.substring(0, marginTopStr.indexOf('px')), 10)
		;		


		//Apply the top and width to fix the position of the element
		this.$el.css('top',  marginTop +'px');
		this.$el.css('width', this.elWidth+'px');

		//The bindWidth parameter uses 'body' as default, 
		//incase user specified an element, then that element will be used instead
		this.elHeight = $(this.options.bindWith).height();

	};



	/**
	 * Update sticky element's style on window.scroll
	 */
	Sticky.prototype.scrollHandler = function() {

		var self = this;

		$(window).on('scroll', function(){

			var windowScrollTop = $(window).scrollTop();

			/**
			 * Change position to fixed when window's scrollTop reaches sticky
			 * and change it back to static when it leaves the element
			 */
			if(windowScrollTop > self.pos.top && windowScrollTop < self.pos.top + self.elHeight) {
				self.$stickyEl.css('position', 'fixed');
			} else {
				self.$stickyEl.css('position', 'static');
			}

		});

	};

	///////////////////////////////////////////////////
	///////////////INITIALIZE THE PLUGIN///////////////
	///////////////////////////////////////////////////
	
	var pluginName = 'sticky';

	$.fn[pluginName] = function(options) {

		return this.each(function() {

			/**
			 * Allow the plugin to be initialized on an element only once
			 * This way we can call the plugin's internal function
			 * without having to reinitialize the plugin all over again.
			 */
			if (!($.data(this, 'plugin_' + pluginName) instanceof Sticky)) {

				/**
				 * Create a new data attribute on the element to hold the plugin name
				 * This way we can know which plugin(s) is/are initialized on the element later
				 */
				$.data(this, 'plugin_' + pluginName, new Sticky(this, options));

			}

			/**
			 * Use the instance of this plugin derived from the data attribute for this element
			 * to conduct whatever action requested as a string parameter.
			 */
			var instance = $.data(this, 'plugin_' + pluginName);

			/**
			 * Provision for calling a function from this plugin
			 * without initializing it all over again
			 */
			if (typeof options === 'string') {
				if (typeof instance[options] === 'function') {
					/**
					 * Pass in 'instance' to provide for the value of 'this' in the called function
					 */
					instance[options].call(instance);
				}
			}


		});
	};

	////////////////////////////////////////////////////
	////////////////////////////////////////////////////


})(jQuery);