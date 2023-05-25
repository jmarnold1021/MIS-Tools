USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_SF]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SF]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_SF]
GO
/****** Object:  Table [dbo].[L56_DOD_SF]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_SF](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[SF01] [varchar](1) NULL,
	[SF02] [varchar](5) NULL,
	[SF03] [varchar](1) NULL,
	[SF04] [int] NULL,
	[SF05] [varchar](1) NULL,
	[SF06] [int] NULL,
	[SF07] [varchar](2) NULL,
	[SF08] [int] NULL,
	[SF09] [int] NULL,
	[SF10] [int] NULL,
	[SF11] [int] NULL,
	[SF17] [int] NULL,
 CONSTRAINT [PK_DOD_SF_GI03_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
