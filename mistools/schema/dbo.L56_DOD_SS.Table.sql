USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_SS]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SS]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_SS]
GO
/****** Object:  Table [dbo].[L56_DOD_SS]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_SS](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[SS01] [varchar](1) NULL,
	[SS02] [varchar](6) NULL,
	[SS03] [varchar](2) NULL,
	[SS04] [varchar](2) NULL,
	[SS05] [varchar](2) NULL,
	[SS06] [varchar](1) NULL,
	[SS07] [varchar](4) NULL,
	[SS08] [varchar](1) NULL,
	[SS09] [varchar](1) NULL,
	[SS10] [varchar](1) NULL,
	[SS11] [varchar](4) NULL,
	[SS12] [varchar](6) NULL,
	[SS13] [varchar](2) NULL,
	[SS14] [varchar](2) NULL,
	[SS15] [varchar](2) NULL,
	[SS16] [varchar](1) NULL,
	[SS17] [varchar](4) NULL,
	[SS18] [varchar](1) NULL,
	[SS19] [varchar](1) NULL,
	[SS20] [varchar](3) NULL,
 CONSTRAINT [PK_DOD_SS_GI03_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
