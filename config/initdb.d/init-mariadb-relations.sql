CREATE TABLE `rel_box_networks` (
  `id`         bigint(20)   NOT NULL AUTO_INCREMENT,
  `network_id` bigint(20)   NOT NULL,
  `box_id`     bigint(20)   NOT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END rel_box_networks table

CREATE TABLE `rel_box_routing` (
  `id`         bigint(20)   NOT NULL AUTO_INCREMENT,
  `routing_id` bigint(20)   NOT NULL,
  `box_id`     bigint(20)   NOT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END rel_box_routing table

CREATE TABLE `rel_box_services` (
  `id`         bigint(20)   NOT NULL AUTO_INCREMENT,
  `service_id` bigint(20)   NOT NULL,
  `box_id`     bigint(20)   NOT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END rel_box_services table

CREATE TABLE `rel_users_endpoints` (
  `id`            bigint(20) NOT NULL AUTO_INCREMENT,
  `users_id`      bigint(20) NOT NULL AUTO_INCREMENT,
  `endpoints_id`  bigint(20) NOT NULL AUTO_INCREMENT,

  PRIMARY KEY (`id`),

  KEY `key_id`            (`id`),
  KEY `key_users_id`      (`users_id`),
  KEY `key_endpoints_id`  (`endpoints_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END rel_users_endpoints

CREATE TABLE `rel_box_endpoints` (
  `id`           bigint(20) NOT NULL AUTO_INCREMENT,
  `box_id`       bigint(20) NOT NULL AUTO_INCREMENT,
  `endpoints_id` bigint(20) NOT NULL AUTO_INCREMENT,

  PRIMARY KEY (`id`),

  KEY `key_id`           (`id`),
  KEY `key_box_id`       (`box_id`),
  KEY `key_endpoints_id` (`endpoints_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END rel_box_endpoints
