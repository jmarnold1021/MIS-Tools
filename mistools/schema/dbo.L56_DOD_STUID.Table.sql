USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_STUID]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_STUID]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_STUID]
GO
/****** Object:  Table [dbo].[L56_DOD_STUID]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_STUID](
	[GI01] [varchar](3) NULL,
	[SB00] [varchar](9) NOT NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[SB01] [varchar](1) NULL,
	[GI03] [varchar](3) NULL,
	[GI03_E] [varchar](5) NULL,
	[SB34] [varchar](8) NULL,
	[SB35] [varchar](10) NULL,
 CONSTRAINT [PK_DOD_STUID_SB00_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[SB00] ASC,
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
