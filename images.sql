CREATE TABLE IF NOT EXISTS `fitmeimages` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `shade` int(11) NOT NULL,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

INSERT INTO `fitmeimages` (`id`, `filename`, `shade`, `x`, `y`) VALUES
(1, 'thumb00.jpg', 8, 5405, 575),
(2, 'thumb02.jpg', 9, 5290, 1380),
(3, 'thumb04.jpg', 4, 5175, 1150),
(4, 'thumb03.jpg', 8, 5290, 1150),
(5, 'thumb05.jpg', 1, 5290, 1265),
(6, 'thumb07.jpg', 3, 5290, 920),
(7, 'thumb01.jpg', 5, 5290, 1035),
(8, 'thumb06.jpg', 6, 5290, 690);

