-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 03, 2023 at 06:23 AM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `status_admin` tinyint(2) NOT NULL COMMENT '1 Aktif, 2 Tidak aktif',
  `waktu_terakhir_login_admin` datetime DEFAULT NULL,
  `is_delete` tinyint(2) NOT NULL DEFAULT 0 COMMENT '0 Tidak dihapus, 1 Dihapus'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id_customer` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `status_customer` tinyint(4) NOT NULL COMMENT '1 Aktif, 2 Tidak aktif',
  `waktu_terakhir_login_customer` datetime DEFAULT NULL,
  `is_delete` tinyint(4) NOT NULL DEFAULT 0 COMMENT '0 Tidak dihapus, 1 Dihapus'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `lndr_cucian`
--

CREATE TABLE `lndr_cucian` (
  `id_cucian` int(11) NOT NULL,
  `id_customer` int(11) NOT NULL,
  `waktu_cucian_masuk` datetime NOT NULL,
  `waktu_cucian_mulai` datetime DEFAULT NULL,
  `waktu_cucian_selesai` datetime DEFAULT NULL,
  `waktu_perkiraan_selesai` datetime NOT NULL,
  `total_harga` int(11) NOT NULL,
  `status_cucian` int(11) NOT NULL COMMENT '1 Menunggu, 2 Proses Cuci, 3 Selesai, 4 Dibatalkan',
  `is_delete` tinyint(2) NOT NULL DEFAULT 0 COMMENT '0 Tidak dihapus, 1 Dihapus'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `lndr_cucian_detail`
--

CREATE TABLE `lndr_cucian_detail` (
  `id_cucian_detail` int(11) NOT NULL,
  `id_cucian` int(11) NOT NULL,
  `id_item` int(11) NOT NULL,
  `jumlah_item` int(11) NOT NULL,
  `harga` int(11) NOT NULL,
  `is_delete` tinyint(2) NOT NULL DEFAULT 0 COMMENT '0 Tidak dihapus, 1 Dihapus'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `lndr_item`
--

CREATE TABLE `lndr_item` (
  `id_item` int(11) NOT NULL,
  `nama_item` varchar(255) NOT NULL,
  `harga` int(11) NOT NULL,
  `harga_diskon` int(11) NOT NULL,
  `is_diskon` tinyint(2) NOT NULL DEFAULT 0 COMMENT '0 Tidak diskon, 1 Diskon',
  `is_delete` tinyint(2) NOT NULL DEFAULT 0 COMMENT '0 Tidak dihapus, 1 Dihapus'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `lndr_transaksi_cucian`
--

CREATE TABLE `lndr_transaksi_cucian` (
  `id_transaksi_cucian` int(11) NOT NULL,
  `id_cucian` int(11) NOT NULL,
  `nomor_invoice` varchar(100) NOT NULL,
  `waktu_transaksi_dibuat` datetime NOT NULL,
  `waktu_transaksi_berakhir` datetime NOT NULL,
  `waktu_transaksi_dibayar` datetime DEFAULT NULL,
  `foto_bukti_pembayaran` varchar(255) NOT NULL,
  `tipe_pembayaran` tinyint(2) NOT NULL COMMENT '1 Tunai, 2 Non tunai',
  `status_pembayaran` tinyint(2) NOT NULL COMMENT '1 Belum, 2 Sudah, 3 Gagal',
  `service_code` varchar(10) DEFAULT NULL,
  `redirect_url` text DEFAULT NULL,
  `redirect_data` longtext DEFAULT NULL,
  `nomor_virtual_account` varchar(30) DEFAULT NULL,
  `is_delete` tinyint(4) NOT NULL DEFAULT 0 COMMENT '0 Tidak dihapus, 1 Dihapus'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(200) NOT NULL,
  `nama_user` varchar(150) NOT NULL,
  `nomor_telfon` varchar(20) DEFAULT NULL,
  `jenis_kelamin` tinyint(2) DEFAULT NULL COMMENT '1 Laki-laki, 2 Perempuan',
  `tanggal_lahir` date DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `foto_user` varchar(255) DEFAULT NULL,
  `status_user` tinyint(2) NOT NULL DEFAULT 1 COMMENT '1 Aktif, 2 Tidak aktif',
  `is_delete` tinyint(2) NOT NULL DEFAULT 0 COMMENT '1 Dihapus, 0 Tidak dihapus'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id_customer`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `lndr_cucian`
--
ALTER TABLE `lndr_cucian`
  ADD PRIMARY KEY (`id_cucian`),
  ADD KEY `id_customer` (`id_customer`);

--
-- Indexes for table `lndr_cucian_detail`
--
ALTER TABLE `lndr_cucian_detail`
  ADD PRIMARY KEY (`id_cucian_detail`),
  ADD KEY `id_cucian` (`id_cucian`),
  ADD KEY `id_item` (`id_item`);

--
-- Indexes for table `lndr_item`
--
ALTER TABLE `lndr_item`
  ADD PRIMARY KEY (`id_item`);

--
-- Indexes for table `lndr_transaksi_cucian`
--
ALTER TABLE `lndr_transaksi_cucian`
  ADD PRIMARY KEY (`id_transaksi_cucian`),
  ADD KEY `id_cucian` (`id_cucian`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id_customer` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `lndr_cucian_detail`
--
ALTER TABLE `lndr_cucian_detail`
  MODIFY `id_cucian_detail` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `lndr_item`
--
ALTER TABLE `lndr_item`
  MODIFY `id_item` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `lndr_transaksi_cucian`
--
ALTER TABLE `lndr_transaksi_cucian`
  MODIFY `id_transaksi_cucian` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `customer`
--
ALTER TABLE `customer`
  ADD CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `lndr_cucian`
--
ALTER TABLE `lndr_cucian`
  ADD CONSTRAINT `lndr_cucian_ibfk_1` FOREIGN KEY (`id_customer`) REFERENCES `customer` (`id_customer`);

--
-- Constraints for table `lndr_cucian_detail`
--
ALTER TABLE `lndr_cucian_detail`
  ADD CONSTRAINT `lndr_cucian_detail_ibfk_1` FOREIGN KEY (`id_cucian`) REFERENCES `lndr_cucian` (`id_cucian`),
  ADD CONSTRAINT `lndr_cucian_detail_ibfk_2` FOREIGN KEY (`id_item`) REFERENCES `lndr_item` (`id_item`);

--
-- Constraints for table `lndr_transaksi_cucian`
--
ALTER TABLE `lndr_transaksi_cucian`
  ADD CONSTRAINT `lndr_transaksi_cucian_ibfk_1` FOREIGN KEY (`id_cucian`) REFERENCES `lndr_cucian` (`id_cucian`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
