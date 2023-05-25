USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_FR]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_FR]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_FR]
GO
/****** Object:  Table [dbo].[L56_DOD_FR]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_FR](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[CCC_GI03] [varchar](3) NULL,
	[CCC_GI03_V] [varchar](5) NULL,
	[CCC_GI03_L] [varchar](1) NULL,
	[CCC_GI03_NSA] [varchar](3) NULL,
	[CCC_GI03_NSA_V] [varchar](5) NULL,
	[CCC_GI03_NSA_L] [varchar](1) NULL,
	[CCC_GI03_CR] [varchar](3) NULL,
	[CCC_GI03_CR_V] [varchar](5) NULL,
	[CCC_GI03_CR_L] [varchar](1) NULL,
	[CCC_GI03_CR_NSA] [varchar](3) NULL,
	[CCC_GI03_CR_NSA_V] [varchar](5) NULL,
	[CCC_GI03_CR_NSA_L] [varchar](1) NULL,
	[CCC_GI03_NCR] [varchar](3) NULL,
	[CCC_GI03_NCR_V] [varchar](5) NULL,
	[CCC_GI03_NCR_L] [varchar](1) NULL,
	[CCC_GI03_NCR_NSA] [varchar](3) NULL,
	[CCC_GI03_NCR_NSA_V] [varchar](5) NULL,
	[CCC_GI03_NCR_NSA_L] [varchar](1) NULL,
	[GI03] [varchar](3) NULL,
	[GI03_V] [varchar](5) NULL,
	[GI03_L] [varchar](1) NULL,
	[GI03_NSA] [varchar](3) NULL,
	[GI03_NSA_V] [varchar](5) NULL,
	[GI03_NSA_L] [varchar](1) NULL,
	[GI03_CR] [varchar](3) NULL,
	[GI03_CR_V] [varchar](5) NULL,
	[GI03_CR_L] [varchar](1) NULL,
	[GI03_CR_NSA] [varchar](3) NULL,
	[GI03_CR_NSA_V] [varchar](5) NULL,
	[GI03_CR_NSA_L] [varchar](1) NULL,
	[DIRECTED_YEAR] [varchar](5) NULL,
	[PREPARED_YEAR] [varchar](5) NULL,
	[FIRST_DATE_4YR] [varchar](8) NULL,
	[FIRST_SEGMENT_4YR] [varchar](3) NULL,
	[LAST_DATE_4YR] [varchar](8) NULL,
	[LAST_SEGMENT_4YR] [varchar](3) NULL,
 CONSTRAINT [PK_DOD_FR_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
