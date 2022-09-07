CREATE TABLE `users` (
  `id`       bigint(20)   NOT NULL AUTO_INCREMENT,
  `fullname` varchar(512) DEFAULT '',
  `signed`   binary(16)   NOT NULL,            -- signed RANDOM hash for signed token
  `uuid`     binary(16)   NOT NULL,            -- uuid RANDOM identified for user
  `email`    varchar(320) NOT NULL,            -- email RFC https://www.rfc-editor.org/rfc/rfc3696
  `pass`     binary(32)   NOT NULL,            -- pass save in bytes using sha256
  `flags`    int(4)       NOT NULL DEFAULT 0,  -- 00000000 00000000 00000000 00000000
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
  `flags`    int(4)        NOT NULL DEFAULT 0,           -- 00000000 00000000 00000000 00000000
  `created`  timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated`  timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END endpoints table

CREATE TABLE `box` (
  `id`            bigint(20)   NOT NULL AUTO_INCREMENT,
  `uuid`          binary(32)   NOT NULL,         -- uuid is a hash sha256 of description, product, cpu_model,
  `hwinfo`        text         NOT NULl DEFAULT '',
  `arch`          varchar(255) NOT NULl DEFAULT '',
  `cpu_model`     varchar(255) NOT NULl DEFAULT '',
  `load_average`  varchar(255) NOT NULL DEFAULT '[0.0, 0.0, 0.0]',
  `ram_total`     int(11)      NOT NULL DEFAULT 0,
  `ram_free`      int(11)      NOT NULL DEFAULT 0,
  `ram_available` int(11)      NOT NULL DEFAULT 0,
  `ram_buffers`   int(11)      NOT NULL DEFAULT 0,
  `ram_cached`    int(11)      NOT NULL DEFAULT 0,
  `created`       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated`       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`),

  UNIQUE KEY `uniq_id`    (`id`),
  UNIQUE KEY `uniq_uuid`  (`uuid`)

) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END box table

CREATE TABLE `networks` (
  `id`             bigint(20)   NOT NULL AUTO_INCREMENT,
  `name`           varchar(64)  NOT NULL DEFAULT '',
  `mac`            binary(8)    NOT NULL,
  `ipv4_addrress`  binary(4)    NOT NULL DEFAULT 0,
  `netmask`        binary(4)    NOT NULL DEFAULT 0,
  `gateway`        binary(4)    NOT NULL DEFAULT 0,

  PRIMARY KEY (`id`),

  UNIQUE KEY `uniq_mac`   (`mac`)

) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END networks table

CREATE TABLE `routing` (
  `id`    bigint(20)   NOT NULL AUTO_INCREMENT,
  `info`  varchar(512) NOT NULL DEFAULT '',

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END routing table

CREATE TABLE `services` (
  `id`         bigint(20)   NOT NULL AUTO_INCREMENT,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END services table

CREATE TABLE `software` (
  `id`          bigint(20)   NOT NULL AUTO_INCREMENT,
  `name`        varchar(255) NOT NULL DEFAULT '',
  `version`     varchar(32)  NOT NULL DEFAULT '',
  `arch`        varchar(32)  NOT NULL DEFAULT '',
  `description` varchar(512) NOT NULL DEFAULT '',

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
-- END software table

CREATE TABLE `sessions` (
  `id`         bigint(20)     NOT NULL AUTO_INCREMENT,
  `uuid`       binary(16)     NOT NULL,
  `starttime`  timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `endtime`    timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `token`      text           DEFAULT NULL,
  `flags`      int(1)         NOT NULL DEFAULT '1',                    -- 00000000

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
