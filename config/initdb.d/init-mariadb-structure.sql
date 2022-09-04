CREATE TABLE `users` (
  `id`       bigint(20)   NOT NULL AUTO_INCREMENT,
  `fullname` varchar(512) DEFAULT '',
  `signed`   binary(16)   NOT NULL,            -- signed RANDOM hash for signed token
  `uuid`     binary(16)   NOT NULL,            -- uuid RANDOM identified for user
  `email`    varchar(320) NOT NULL,            -- email RFC https://www.rfc-editor.org/rfc/rfc3696
  `pass`     binary(32)   NOT NULL,            -- pass save in bytes using sha256
  `flags`    int(4)       NOT NULL DEFAULT 0,  -- flags 00000000 00000000 00000000 00000000
  `created`  timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated`  timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

PRIMARY KEY (`id`),

UNIQUE KEY `uniq_id`    (`id`),
UNIQUE KEY `uniq_email` (`email`),
UNIQUE KEY `uniq_uid`   (`uuid`),

KEY `key_id`      (`id`),
KEY `key_uuid`    (`uuid`),
KEY `key_email`   (`email`),
KEY `key_signed`  (`signed`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END users table

CREATE TABLE `endpoints` (
  `id`       bigint(20)    NOT NULL AUTO_INCREMENT,
  `path`     varchar(255)  NOT NULL,
  `flags`    int(4)        NOT NULL DEFAULT 0,           -- Flags 00000000 00000000 00000000 00000000
  `created`  timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated`  timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END endpoints table

CREATE TABLE `toolbox` (
  `id`       bigint(20)   NOT NULL AUTO_INCREMENT,
  `type`     int(1)       NOT NULL DEFAULT 0,         -- 00000000
  `flags`    int(4)       NOT NULL DEFAULT 0,         -- Flags 00000000 00000000 00000000 00000000
  `created`  timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated`  timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END toolbox table

CREATE TABLE `rel_users_endpoints` (
  `id`            bigint(20) NOT NULL AUTO_INCREMENT,
  `users_id`      bigint(20) NOT NULL AUTO_INCREMENT,
  `endpoints_id`  bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),


  KEY `key_id`            (`id`),
  KEY `key_users_id`    (`users_id`),
  KEY `key_endpoints_id`  (`endpoints_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END rel_users_endpoints

CREATE TABLE `rel_toolbox_endpoints` (
  `id`            bigint(20) NOT NULL AUTO_INCREMENT,
  `toolbox_id`    bigint(20) NOT NULL AUTO_INCREMENT,
  `endpoints_id`  bigint(20) NOT NULL AUTO_INCREMENT,

  PRIMARY KEY (`id`),

  KEY `key_id`            (`id`),
  KEY `key_toolbox_id`    (`toolbox_id`),
  KEY `key_endpoints_id`  (`endpoints_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END rel_toolbox_endpoints

CREATE TABLE `sessions` (
  `id`         bigint(20)     NOT NULL AUTO_INCREMENT,
  `uuid`       binary(16)     NOT NULL,
  `starttime`  timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `endtime`    timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `token`      text           DEFAULT NULL,
  `flags`      int(1)         NOT NULL DEFAULT '1',                    -- Flags 00000000

  PRIMARY KEY (`id`),

  UNIQUE KEY `uniq_id` (`id`),

  KEY `key_id`     (`id`),
  KEY `key_uuid`   (`uuid`),
  KEY `key_start`  (`starttime`),
  KEY `key_end`    (`endtime`),
  KEY `key_flags`  (`flags`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END sessions table

CREATE TABLE `devices` (
  `id`       bigint(20)  NOT NULL AUTO_INCREMENT,
  `flags`    int(4)      NOT NULL DEFAULT 0,           -- Flags 00000000 00000000 00000000 00000000
  `created`  timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated`  timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END devices table
