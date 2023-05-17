-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
/*START TRANSACTION;*/
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contacts`
--

CREATE TABLE `contacts` (
  `id` int(11) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `phone` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `int_ref`
--

CREATE TABLE `int_ref` (
  `id_product` int(11) DEFAULT NULL,
  `id_odoo` int(11) NOT NULL,
  `id_wc` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Estructura de tabla para la tabla `int_ref_products`
--

CREATE TABLE `int_ref_products` (
  `id_order_int` int(11) NOT NULL,
  `id_product` int(11) NOT NULL,
  `id_order` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Estructura de tabla para la tabla `orders`
--

CREATE TABLE `orders` (
  `id_order_int` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `subtotal_price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `id_product` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `regular_price` float NOT NULL,
  `description` text DEFAULT NULL,
  `short_description` varchar(255) DEFAULT NULL,
  `categories` varchar(255) DEFAULT NULL,
  `images` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Estructura de tabla para la tabla `sales`
--

CREATE TABLE `sales` (
  `id` int(11) NOT NULL,
  `id_order` int(11) NOT NULL,
  `total_sale_price` decimal(10,2) DEFAULT NULL,
  `sh_name` varchar(255) DEFAULT NULL,
  `sh_surnames` varchar(255) DEFAULT NULL,
  `sh_company` varchar(255) DEFAULT NULL,
  `sh_address1` varchar(255) DEFAULT NULL,
  `sh_address2` varchar(255) DEFAULT NULL,
  `sh_city` varchar(255) DEFAULT NULL,
  `sh_state` varchar(255) DEFAULT NULL,
  `sh_postcode` varchar(255) DEFAULT NULL,
  `sh_country` varchar(255) DEFAULT NULL,
  `sh_email` varchar(255) DEFAULT NULL,
  `sh_phone` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indices de la tabla `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `int_ref`
--
ALTER TABLE `int_ref`
  ADD PRIMARY KEY (`id_odoo`),
  ADD KEY `id_product` (`id_product`);

--
-- Indices de la tabla `int_ref_products`
--
ALTER TABLE `int_ref_products`
  ADD PRIMARY KEY (`id_order_int`),
  ADD KEY `fk_ref_products` (`id_product`),
  ADD KEY `fk_ref_orders` (`id_order`);

--
-- Indices de la tabla `orders`
--
ALTER TABLE `orders`
  ADD KEY `fk_int_ref_products_orders` (`id_order_int`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id_product`);

--
-- Indices de la tabla `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_sales_int_ref_prducts` (`id_order`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `int_ref_products`
--
ALTER TABLE `int_ref_products`
  MODIFY `id_order_int` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `id_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1252;

--
-- AUTO_INCREMENT de la tabla `sales`
--
ALTER TABLE `sales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `int_ref`
--
ALTER TABLE `int_ref`
  ADD CONSTRAINT `int_ref_ibfk_1` FOREIGN KEY (`id_product`) REFERENCES `products` (`id_product`);

--
-- Filtros para la tabla `int_ref_products`
--
ALTER TABLE `int_ref_products`
  ADD CONSTRAINT `fk_ref_products` FOREIGN KEY (`id_product`) REFERENCES `int_ref` (`id_product`);

--
-- Filtros para la tabla `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `fk_int_ref_products_orders` FOREIGN KEY (`id_order_int`) REFERENCES `int_ref_products` (`id_order_int`);

--
-- Filtros para la tabla `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `fk_sales_int_ref_prducts` FOREIGN KEY (`id_order`) REFERENCES `int_ref_products` (`id_order`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
