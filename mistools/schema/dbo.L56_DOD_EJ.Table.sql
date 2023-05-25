USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_EJ]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_EJ]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_EJ]
GO
/****** Object:  Table [dbo].[L56_DOD_EJ]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_EJ](
	[GI01] [varchar](6) NULL,
	[GI03] [varchar](3) NOT NULL,
	[EB00] [varchar](9) NOT NULL,
	[EJ01] [varchar](2) NOT NULL,
	[EJ02] [varchar](1) NULL,
	[EJ03] [varchar](6) NOT NULL,
	[EJ03B] [varchar](1) NULL,
	[EJ04] [decimal](3, 1) NULL,
	[EJ05] [decimal](5, 2) NULL,
	[EJ08] [decimal](5, 2) NULL,
 CONSTRAINT [PK_DOD_EJ_GI03_EB00_EJ01_EJ03] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[EB00] ASC,
	[EJ01] ASC,
	[EJ03] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
